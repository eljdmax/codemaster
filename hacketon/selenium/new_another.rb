require "selenium-webdriver"
require 'uri'
require 'net/http'
require 'http/cookie'

$folder = "/home/rob/code/selenium"
$file = "#{$folder}/list"
$processed = "#{$folder}/processed"
$failed  = "#{$folder}/failed"

$cookies_folder = $folder + "/cookies"

$line = `head -n 1 #{$file}`

if $line.to_s.empty?
   abort "nothing to process"
end


$line = $line.chomp

$wait = Selenium::WebDriver::Wait.new(:timeout => 60) #second
$waitLong = Selenium::WebDriver::Wait.new(:timeout => 120) #second
$waitShort = Selenium::WebDriver::Wait.new(:timeout => 10) #second



Selenium::WebDriver::Firefox::Binary.path = "/home/rob/Downloads/firefox-sdk/bin/firefox"
#Selenium::WebDriver::Firefox::Binary.path = "/root/Downloads/firefox-51.0.linux-i686.sdk/firefox-sdk/bin/firefox" 

profile = Selenium::WebDriver::Firefox::Profile.from_name "default"
#profile.add_extension('/root/Downloads/firefox-48.0.linux-i686.sdk/firefox-sdk/bin/browser/extensions/{972ce4c6-7e08-4474-a285-3208198ce6fd}.xpi')

options = Selenium::WebDriver::Firefox::Options.new(profile: profile, log_level: :trace)

#Selenium::WebDriver::logger.level = :debug
$driver = Selenium::WebDriver.for :firefox, :options => options #, :profile => $default_profile

$driver.manage.delete_all_cookies

def wait_for(type , locator, delta = 30)

   startTime = Time.now.to_i 
   while (Time.now.to_i  < startTime + delta)
      begin
         if (type == 'id') 
            cond = $driver.find_element(id: locator).displayed?
         elsif (type == 'css')
            cond = $driver.find_element(css: locator).displayed?
	 elsif (type == 'id-check')
            cond =  ($driver.find_element(id: locator).attribute('aria-checked') == 'true') ? true : false
         else
            cond = false
         end

         if ( cond )
             puts "#{locator} is displayed now"
             return 
         else
             sleep(0.2)
         end
      rescue Exception => e
         sleep(0.2)
      end
   end
   raise "wait for timed out"
end


def optionSelect(my_select, value)

    sleep 0.5 
    my_select.click
    sleep 0.5
    my_select.find_elements( :tag_name => "option" ).find do |option|
      option.attribute('value') == value
    end.click

end

def goToRef()

    $url = 'https://refereum.com/?refid=367blgezsk'
    $signUpId = 'landing-save-button'
    $acceptId = 'acceptTerms'
    $twitchId = 'twitchSignIn'
    $discordId = 'discordSignIn'
    $authorizeId = 'button.button.js-authorize' 

    begin 
        $driver.navigate.to $url
        sleep(5)
        wait_for('id' ,  $signUpId)
        $driver.find_element(id: $signUpId).click
    rescue Exception => e
        puts "second..."
        $driver.navigate.to $url
        sleep(5)    
        wait_for('id' ,  $signUpId)
        $driver.find_element(id: $signUpId).click
    end

    wait_for( 'id' , $acceptId)
    $driver.find_element(id: $acceptId).send_keys(:space)

    wait_for('id' ,  $twitchId)
    $driver.find_element(id: $twitchId).click
  
    wait_for('css', $authorizeId)
    sleep(7)
    wait_for('css', $authorizeId)

    $driver.find_element(css: $authorizeId).send_keys(:enter)

end

def processTwitch(user, email)

    $usernameId = '#signupForm #username'
    $passwordId = '#signupForm #password'
    $dateMonthId = '#signupForm select[name="birthday.month"]'
    $dateDayId = '#signupForm select[name="birthday.day"]'
    $dateYearId = '#signupForm select[name="birthday.year"]'  
    $emailId = '#signupForm input[name=email]'
    $submitId = 'button[type=submit]'

    $frame  = '#g-recaptcha iframe'
    $recaptcha  = 'recaptcha-anchor';
    $responsecap = "#g-recaptcha-response"

    $signUpUrl ='https://www.twitch.tv/signup'

    $driver.navigate.to $signUpUrl 

    wait_for('css', $usernameId)
    $driver.find_element(css: $usernameId).send_keys(user)

    wait_for('css', $passwordId)
    $driver.find_element(css: $passwordId).send_keys("Master@123")

    
    month = rand(1..12)
    optionSelect($driver.find_element(css: $dateMonthId), month.to_s)

    day = rand(1..28)
    optionSelect($driver.find_element(css: $dateDayId), day.to_s)

    year = rand(1977..1994)
    optionSelect($driver.find_element(css: $dateYearId), year.to_s)  

    wait_for('css', $emailId)
    $driver.find_element(css: $emailId).send_keys(email)


    $dropId = 'button[data-a-target=user-menu-toggle]'

    begin
      wait_for('css', $dropId,45)
    rescue Exception => e
    end


end

def twitchExit()

    $url = 'https://www.twitch.tv/directory/'
    $dropId = 'button[data-a-target=user-menu-toggle]'
    $logOutId = 'button[data-a-target=dropdown-logout]'

    $driver.navigate.to $url
    wait_for('css', $dropId)
    $driver.find_element(css: $dropId).send_keys(:enter) 

    wait_for('css', $logOutId)
    $driver.find_element(css: $logOutId).send_keys(:enter)
    sleep(5)

end


def extraPoints(name)

    $accountLink = 'https://refereum.com/Account'

    $editId = 'a#account-text-edit-button'
    $ethTextId = 'input#ethereumAddress'
    $saveId = 'a#account-text-save-button'
    $address = '0x80d2c1050F5a3D84f4C8dC467c119F06B311F3d0'

    begin
      $driver.navigate.to $accountLink
      wait_for('css', $editId)
      $driver.find_element(css: $editId).click
      wait_for('css', $ethTextId)
      $driver.find_element(css: $ethTextId).send_keys($address)
      sleep(0.5)
      wait_for('css', $saveId,10)
      $driver.find_element(css: $saveId).click
    rescue Exception => e
    end


    cookie = $cookies_folder + '/ref/ref_'+name+'.txt'

    jar = HTTP::CookieJar.new
    jar.load(cookie, :format => :cookiestxt)

    http = Net::HTTP.new('refereum.com',443)
    http.use_ssl = true

    header = { "Cookie" => HTTP::Cookie.cookie_value(jar.cookies()),
               "Accept" => "*/*",
               "Accept-Encoding" => "gzip, deflate, br",
               "Accept-Language" => "en-US,en;q=0.5",
               "Connection" => "keep-alive",
               "Host" => "refereum.com",
               "Upgrade-Insecure-Requests" => "1",
               "User-Agent" => "Mozilla/5.0 (X11; Linux i686; rv:58.0) Gecko/20100101 Firefox/58.0"
    }

    path = '/Home/RedditFollow'
    begin
      content =''
      resp = http.get(path,header) do |str|
          content += str
      end
    rescue Exception => e
    end

    sleep(1)

    path = '/Home/TwitterFollow'
    begin
      content =''
      resp = http.get(path,header) do |str|
          content += str
      end
    rescue Exception => e
    end

    sleep(1)

    path = '/Home/FacebookFollow'
    begin
      content =''
      resp = http.get(path,header) do |str|
          content += str
      end
    rescue Exception => e
    end

    sleep(1)

    path = '/Home/TwitterShareRfr'
    begin
      content =''
      resp = http.get(path,header) do |str|
          content += str
      end
    rescue Exception => e
    end

    sleep(1)

    path = '/Home/FacebookShareRfr'
    begin
      content =''
      resp = http.get(path,header) do |str|
          content += str
      end
    rescue Exception => e
    end

    sleep(1)

    path = '/Home/TwitterShareOkEx'
    begin
      content =''
      resp = http.get(path,header) do |str|
          content += str
      end
    rescue Exception => e
    end

    sleep(1)

    path = '/Home/FacebookShareOkEx'
    begin
      content =''
      resp = http.get(path,header) do |str|
          content += str
      end
    rescue Exception => e
    end

    sleep(1)

    path = '/Home/TwitterRetweetRfr'
    begin
      content =''
      resp = http.get(path,header) do |str|
          content += str
      end
    rescue Exception => e
    end

    sleep(1)

    path = '/Home/TwitterRetweetOkEx'
    begin
      content =''
      resp = http.get(path,header) do |str|
          content += str
      end
    rescue Exception => e
    end

    sleep(1)

    path = '/Vid/Watched'
    begin
      content =''
      resp = http.post(path,nil,header) do |str|
          content += str
      end
    rescue Exception => e
    end

end


def snapshot(name,prefix)

    newFolder = $cookies_folder + '/'+prefix
    newFile = prefix+'_'+name+'.txt'

    puts prefix + " snapshot"

    File.open(newFolder+'/'+newFile, "wb") { |file|
        file.write("#" + name + "\n")
        $driver.manage.all_cookies().each do |cookie|
            secure = "FALSE"
            if cookie[:secure]  then
                secure = "TRUE"
            end
            expires = "0"
            if cookie[:expires] != nil then
                expires = cookie[:expires].to_s
            end
            file.write(cookie[:domain] + "\t" + "TRUE" + "\t" + cookie[:path] + "\t" + secure + "\t" + expires + "\t" + cookie[:name] + "\t" + cookie[:value].to_s + "\n")
        end
    }

   `echo '#{newFile}' >> #{newFolder}/index` 

end

begin

vals = $line.split(',')

processTwitch(vals[0] , vals[1])

snapshot(vals[0],'twi')

sleep(5)

goToRef()

sleep(5)

snapshot(vals[0],'ref')

sleep(5)

extraPoints(vals[0])

sleep(5)

#twitchExit()

puts "end"



`echo '#{$line}' >> #{$processed}`
rescue Exception => e
#clean up
puts "error ... #{e}"
`echo '#{$line}' >> #{$failed}`
end

`sed -i '1d' #{$file}`
$driver.manage.delete_all_cookies
$driver.quit

sleep(2)

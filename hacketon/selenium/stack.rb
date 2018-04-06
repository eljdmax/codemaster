require "selenium-webdriver"
require 'uri'
require 'net/http'
require 'http/cookie'


$folder = "/root/Selenium"

$processed = "#{$folder}/processed"
$failed  = "#{$folder}/failed"

$cookies_folder = $folder + "/cookies"
$index_stack = $cookies_folder +"/twi/index_stack" 

#path = "/home/rlekane/Downloads/firefox-sdk-51/bin/firefox"
$path = "/root/Downloads/firefox-51.0.linux-i686.sdk/firefox-sdk/bin/firefox" 

$profile = Selenium::WebDriver::Firefox::Profile.from_name "default" 

Selenium::WebDriver.logger.level = :fatal

capabilities = Selenium::WebDriver::Remote::Capabilities.firefox(firefox_profile: $profile, firefox_binary: $path, log_level: "fatal", loggingPrefs: '{"loggingPrefs": {"driver": "OFF", "server": "OFF", "browser": "OFF", "addons.xpi": "OFF", "ALL":"OFF" } }' )

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
        wait_for('id' ,  $signUpId,10)
        $driver.find_element(id: $signUpId).click
    rescue Exception => e
        $driver.navigate.to $url
        sleep(5)
        wait_for('id' ,  $signUpId,10)      
        $driver.find_element(id: $signUpId).click
    end

    $usernameId = '#loginForm #username'
    $passwordId = '#loginForm #password'
    $submitId = 'button[type=submit]'

    wait_for( 'id' , $acceptId)
    $driver.find_element(id: $acceptId).send_keys(:space)

    wait_for('id' ,  $twitchId)
    $driver.find_element(id: $twitchId).click


    begin
      wait_for('css', $authorizeId,15)
    rescue Exception => e
    end
    sleep(5)
    wait_for('css', $authorizeId)

    $driver.find_element(css: $authorizeId).send_keys(:enter)

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


def extraPoints(name)

    $accountLink = 'https://refereum.com/Account'

    $editId = 'a#account-text-edit-button'
    $ethTextId = 'input#ethereumAddress'
    $saveId = 'a#account-text-save-button'
    $address = '0x80d2c1050F5a3D84f4C8dC467c119F06B311F3d0'

    begin
      begin
      $driver.navigate.to $accountLink
      wait_for('css', $editId)
      $driver.find_element(css: $editId).click
      rescue Exception => e
          $driver.navigate.to $accountLink
          wait_for('css', $editId)
          $driver.find_element(css: $editId).click
      end
      wait_for('css', $ethTextId)
      $driver.find_element(css: $ethTextId).send_keys($address)
      sleep(0.5)
      wait_for('css', $saveId,10)
      $driver.find_element(css: $saveId).click
    rescue Exception => e
      
    end

    snapshot(name,'ref')
    sleep(5)    

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


def toCookie(line)

   cookie = {}
   tmp = line.split("\t")

   ckd = tmp[0]
   ckd.gsub!(/^\./,'')

   cookie[:domain] = ckd
   cookie[:path] = tmp[2]
   
   if (tmp[3] == "TRUE") then
     cookie[:secure] = true
   end 

   cookie[:name] = tmp[5]
   cookie[:value] = tmp[6]

   return cookie
end


#Main

$driver = Selenium::WebDriver.for :remote, url: "http://localhost:4445/wd/hub", desired_capabilities: capabilities
$driver.manage.delete_all_cookies

File.open($index_stack, "r") do |f|
  f.each_line do |line|   
     line = line.chomp
     begin
        
        if line =~ /twi_([^.]+)\.txt/ then
            name = $1

            begin
              $driver.manage.timeouts.page_load = 12
              $driver.navigate.to  "https://www.twitch.tv/category"
            rescue Exception => e
            end

            $driver.manage.delete_all_cookies
 
            File.open( $cookies_folder+"/twi/"+line, "r") do |c|
               c.each_line do |lc|
                 lc = lc.chomp
                 if lc !~ /^\#/ then
                    begin
                       $driver.manage.add_cookie( toCookie(lc) )
                    rescue Exception => e
                    end
                 end
               end
            end

            goToRef()
            #puts "Done"

            sleep(15)

            extraPoints(name)
            
            $driver.manage.delete_all_cookies

            ##sleep(5)

        end
     rescue Exception => e
       puts e
       `echo '#{line}' >> #{$failed}` 
     end
  end
end


$driver.manage.delete_all_cookies
$driver.quit

`cat /dev/null > #{$index_stack}`

sleep(2)

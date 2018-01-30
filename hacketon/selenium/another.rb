require "selenium-webdriver"

$folder = "/home/rlekane/selenium"
$file = "#{$folder}/list"
$processed = "#{$folder}/processed"
$failed  = "#{$folder}/failed"

$line = `head -n 1 #{$file}`

if $line.to_s.empty?
   abort "nothing to process"
end


$line = $line.chomp

$wait = Selenium::WebDriver::Wait.new(:timeout => 60) #second
$waitLong = Selenium::WebDriver::Wait.new(:timeout => 120) #second
$waitShort = Selenium::WebDriver::Wait.new(:timeout => 10) #second



Selenium::WebDriver::Firefox::Binary.path = "/home/rlekane/Downloads/firefox-sdk-51/bin/firefox"
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

    sleep 1 
    my_select.click
    sleep 1
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

    $driver.navigate.to $url

    wait_for('id' ,  $signUpId)
    $driver.find_element(id: $signUpId).click

    wait_for( 'id' , $acceptId)
    $driver.find_element(id: $acceptId).send_keys(:space)

    wait_for('id' ,  $twitchId)
    $driver.find_element(id: $twitchId).click
  
    sleep(10)
    wait_for('css', $authorizeId)
    sleep(6)
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

    $signUpUrl ='https://passport.twitch.tv/signup/new?client_id=36926892495301a63b2e9350a38d3d6dbf72ad81e571a3ebba4687250ec8f352c70b3e91229602f73e1335528f3caa00a5cf513f484d7003784e722f2ce7a216&embed=0&error_code=&redirect_path=https%3A%2F%2Fwww.twitch.tv%2F&style=&sudo_reason=&username='

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

    wait_for('css', $frame)

    sleep(45)
    
    wait_for('css', $submitId)
    $driver.find_element(css: $submitId).send_keys(:enter)
    sleep(45)

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

def extraPoints()

    $shareLink = 'https://refereum.com/Share'
    $accountLink = 'https://refereum.com/Account'
    $redditId = 'a#RedditFollow'
    $twitterId = 'a#TwitterFollow'
    $facebookId = 'a#FacebookFollow'
    $logoutId = 'a.btn-account-user-profile-action.white'
    $mainWindow = $driver.window_handle
 
    $driver.navigate.to $shareLink
    sleep(5)
    wait_for('css', $redditId)
    $driver.find_element(css: $redditId).click
    sleep(3)

    $driver.switch_to.window($mainWindow)
    $driver.navigate.to $shareLink
    sleep(5)
    wait_for('css', $twitterId)
    $driver.find_element(css: $twitterId).click
    sleep(3)

    $driver.switch_to.window($mainWindow)
    $driver.navigate.to $shareLink
    sleep(5)
    wait_for('css', $facebookId)
    $driver.find_element(css: $facebookId).click
    sleep(3)

    $driver.switch_to.window($mainWindow)
    $driver.navigate.to $accountLink   
    sleep(5)
    wait_for('css', $logoutId)
    $driver.find_element(css: $logoutId).click

end

begin

vals = $line.split(',')

processTwitch(vals[0] , vals[1])

sleep(10)

goToRef()

sleep(10)

extraPoints()

sleep(5)

twitchExit()

sleep(5)
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

sleep(5)

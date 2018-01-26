require "selenium-webdriver"

$folder = "/home/rlekane/selenium"
$file = "#{$folder}/tokens"

$line = `head -n 1 #{$file}`

if $line.to_s.empty?
   abort "nothing to process"
end

$line = $line.chomp

$wait = Selenium::WebDriver::Wait.new(:timeout => 60) #second
$waitLong = Selenium::WebDriver::Wait.new(:timeout => 120) #second
$waitShort = Selenium::WebDriver::Wait.new(:timeout => 10) #second



$url = 'https://refereum.com/?refid=367blgezsk'
$signUpId = 'landing-save-button'
$acceptId = 'acceptTerms'
$twitchId = 'twitchSignIn'
$discordId = 'discordSignIn'

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

def processTwitch(user, email)

    $signUpId = 'signup_tab'
    $signUpCss = '#signup_tab > a:nth-child(1)' 
    $usernameId = '#signupForm #username'

    $frame  = '#g-recaptcha iframe'
    $recaptcha  = 'recaptcha-anchor';
    $responsecap = "#g-recaptcha-response"

    wait_for('id' ,  $twitchId)
    #$wait.until{ $driver.find_element(id: $twitchId).displayed?  }
    $driver.find_element(id: $twitchId).click

    wait_for('css', $frame)
    sleep(20)

    wait_for('css', $signUpCss) 
    #$waitLong.until{ $driver.find_element(id: $signUpId).displayed?  }
    $driver.find_element(css: $signUpCss).click

    wait_for('css', $usernameId)
    #$wait.until{ $driver.find_element(id: $usernameId) }
    $driver.find_element(css: $usernameId).send_keys(user)

    wait_for('css', $passwordId)
    #$wait.until{ $driver.find_element(id: $passwordId).displayed? }
    $driver.find_element(css: $passwordId).send_keys("Master@123")

    
    #$wait.until{ $driver.find_element(css: $dateMonthId).displayed? }  
    month = rand(1..12)
    optionSelect($driver.find_element(css: $dateMonthId), month.to_s)

    #$wait.until{ $driver.find_element(css: $dateDayId).displayed? }  
    day = rand(1..28)
    optionSelect($driver.find_element(css: $dateDayId), day.to_s)

    #$wait.until{ $driver.find_element(css: $dateYearId).displayed? }  
    year = rand(1977..1994)
    optionSelect($driver.find_element(css: $dateYearId), year.to_s)  

    wait_for('css', $emailId)
    #$wait.until{ $driver.find_element(css: $emailId).displayed? }
    $driver.find_element(css: $emailId).send_keys(email)

    wait_for('css', $frame)
    sleep(15)

    element = $driver.find_element(css: $responsecap)
    #puts "value = #{element.attribute('value')}\n"
    #puts "innerHTML = #{element.attribute('innerHTML')}\n"
    curUrl = $driver.current_url
    proxy = "--proxy http://proxy.sdc.hp.com:8080"
    token = "curl #{proxy} -F p=nocaptcha  -F googlekey=6Ld65QcTAAAAAMBbAE8dkJq4Wi4CsJy7flvKhYqX  -F 'pageurl=#{curUrl}' -F key=aede46c8aa5e56deb209676bc2d73089 -F secret=f872b0d3  http://api.captchasolutions.com/solve"
    token.chomp
 
    puts "token = #{token}"
    $driver.execute_script(" arguments[0].value = arguments[1];", element, token)
    $driver.execute_script(" arguments[0].innerHTML = arguments[1];", element, token)
    
    #puts "value = #{element.attribute('value')}\n"
    #puts "innerHTML = #{element.attribute('innerHTML')}\n"

    sleep(5)
    wait_for('css', $submitId)
    #$wait.until{ $driver.find_element(css: $submitId).displayed? }
    $driver.find_element(css: $submitId).send_keys(:enter)

    sleep(10)
    wait_for('css', $authorizeId)
    #$wait.until{ $driver.find_element(css: $authorizeId).displayed? }
    sleep(6)
    wait_for('css', $authorizeId)
    #$waitShort.until{ $driver.find_element(css: $authorizeId).displayed? }

    $driver.find_element(css: $authorizeId).send_keys(:enter)

end


begin

$driver.navigate.to $url

wait_for('id' ,  $signUpId)
#$wait.until{ $driver.find_element(id: $signUpId).displayed? }
$driver.find_element(id: $signUpId).click

wait_for( 'id' , $acceptId)
#$wait.until{ $driver.find_element(id: $acceptId).displayed? }
$driver.find_element(id: $acceptId).send_keys(:space)

processTwitch()

sleep(10)

puts "end"

rescue Exception => e
#clean up
puts "error ... #{e}"
end

$driver.manage.delete_all_cookies
$driver.quit

sleep(5)
`killall -9 firefox 2>/dev/null`
sleep(2)

require "selenium-webdriver"


Selenium::WebDriver::Firefox::Binary.path = "/home/rob/Downloads/firefox-sdk/bin/firefox"
#Selenium::WebDriver::Firefox::Binary.path = "/root/Downloads/firefox-51.0.linux-i686.sdk/firefox-sdk/bin/firefox" 

profile = Selenium::WebDriver::Firefox::Profile.from_name "default"

options = Selenium::WebDriver::Firefox::Options.new(profile: profile, log_level: :trace)

$driver = Selenium::WebDriver.for :firefox, :options => options #, :profile => $default_profile

def wait_for(type , locator, delta = 30)

   startTime = Time.now.to_i 
   while (Time.now.to_i  < startTime + delta)
      begin
         if (type == 'id') 
            cond = $driver.find_element(id: locator).displayed?
         elsif (type == 'css')
            cond = $driver.find_element(css: locator).displayed?
	 elsif (type == 'id-inner')
            cond =  ($driver.find_element(id: locator).attribute('innerHTML') =~ /^Quality:/) ? true : false
         else
            cond = false
         end

         if ( cond )
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


begin
    $inputId = 'input-url'
    $button = 'go'
    $result = 'alert_result'

    $driver.navigate.to "https://pwn.sh/tools/getstream.html"
    wait_for('id', $inputId)
    $driver.find_element(id: $inputId).send_keys("https://www.twitch.tv/makncheesetv")
    $driver.find_element(id: $button).send_keys(:enter)
    
    wait_for('id-inner', $result)
    res = $driver.find_element(id: $result).attribute("innerHTML")
    
    regex = Regexp.new(/.*\[<a\s+href="(.*)">audio_only<\/a>\]/)
    if regex.match(res)
        puts "OK: #{$1}"
    end

rescue Exception => e
#clean up
puts "error ... #{e}"
end

$driver.manage.delete_all_cookies
$driver.quit


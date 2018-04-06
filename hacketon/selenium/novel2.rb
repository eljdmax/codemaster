require "selenium-webdriver"
require 'uri'
require 'net/http'
require 'http/cookie'


$folder = "/root/Selenium"
$file = "#{$folder}/list"
$processed = "#{$folder}/processed"
$failed  = "#{$folder}/failed_stack"

$proxy  = "#{$folder}/proxy"

$cookies_folder = $folder + "/cookies"

$mutex = '/tmp/mutex.m'

def acquire( delta = 60)
   startTime = Time.now.to_i 
   while (Time.now.to_i  < startTime + delta)
      begin
         present = `mkdir #{$mutex} 2>&1`
         present = present.chomp
         if ( present.to_s.empty?)
             return
         else
             sleep(0.5)
         end
      rescue Exception => e
         sleep(0.5)
      end
   end
   raise "wait for timed out"
end

def release()
    `rm -rf #{$mutex}`
end


if (ARGV[0])
    prof = ARGV[0]
else
    prof = "default"
end


#path = "/home/rlekane/Downloads/firefox-sdk-51/bin/firefox"
$path = "/root/Downloads/firefox-51.0.linux-i686.sdk/firefox-sdk/bin/firefox" 

$profile = Selenium::WebDriver::Firefox::Profile.from_name prof


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


def optionSelect(my_select, value)

    sleep 0.3 
    my_select.click
    sleep 0.3 
    my_select.find_elements( :tag_name => "option" ).find do |option|
      option.attribute('value') == value
    end.click

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

    begin 
      $driver.navigate.to $signUpUrl 
    rescue Exception => e
      $driver.navigate.to $signUpUrl 
    end

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
  
    #sleep(10)
    #wait_for('css', $submitId )
    #$driver.find_element(css: $submitId) .send_keys(:enter)


    $dropId = 'button[data-a-target=user-menu-toggle]'

    begin
    wait_for('css', $dropId, 100)
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

   `echo '#{newFile}' >> #{newFolder}/index_stack` 

end


#MAIN

$driver = Selenium::WebDriver.for :remote, url: "http://localhost:4445/wd/hub", desired_capabilities: capabilities

while true

   begin
     acquire()
     $line = `head -n1 #{$file}`
     `sed -i '1d' #{$file}`
     release()
  
  
      if $line.to_s.empty?
  	   abort "nothing to process"
      end
  
      $line = $line.chomp
  
      vals = $line.split(',')
  
      $driver.manage.delete_all_cookies
  
      begin
        $driver.manage.timeouts.page_load = 40
      rescue Exception => e
      end
  
      processTwitch(vals[0] , vals[1])
  
      sleep(2)
  
      snapshot(vals[0],'twi')
  
      sleep(5)

      $driver.manage.delete_all_cookies
      $driver.navigate.to "about:config"
            

    rescue Exception => e
        puts "error ... #{e}"
        `echo '#{$line}' >> #{$failed}`
    end

    sleep 30+60*2
end

puts "end"


$driver.manage.delete_all_cookies
$driver.quit

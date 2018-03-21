require 'net/http'
require 'json'

$inputFile = '/tmp/mt0'

if ARGV[0] then
  $inputFile = ARGV[0]
end

$domain = '@hotmail.com'

$alpha = 'abcdefghijklmnopqrstuvwzxy'
$xalphan = 'abcdefghijklmnopqrstuvwzxy0123456789'

$la = $alpha.length - 1
$lx = $xalphan.length - 1

$http = Net::HTTP.new('signup.live.com',443)
$http.use_ssl = true

path = '/signup?lcid=1033&wa=wsignin1.0&rpsnv=13&ct=1521626980&rver=6.7.6640.0&wp=MBI_SSL&wreply=https%3a%2f%2foutlook.live.com%2fowa%2f%3fnlp%3d1%26signup%3d1%26RpsCsrfState%3d1b337a4b-babc-6e10-d7b3-2572116515fa&id=292841&CBCXT=out&lw=1&fl=dob%2cflname%2cwld&cobrandid=90015&uaid=5cda43d468f84220aeeab956bee70de0&lic=1'

$full = ''
resp, data = $http.get(path) do |str|
   $full += str
end

$cookie = resp["set-cookie"].split(";")[0]

#puts $cookie

if $full =~ /\$Config=(.*);window\./
  $config = JSON.parse($1)
else
  puts "cant get base config"
  exit 1
end


def isUsed(account)
  path = '/API/CheckAvailableSigninNames?lcid=1033&wa=wsignin1.0&rpsnv=13&ct=1521626980&rver=6.7.6640.0&wp=MBI_SSL&wreply=https://outlook.live.com/owa/?nlp=1&signup=1&RpsCsrfState=1b337a4b-babc-6e10-d7b3-2572116515fa&id=292841&CBCXT=out&lw=1&fl=dob,flname,wld&cobrandid=90015&uaid=5cda43d468f84220aeeab956bee70de0&lic=1'
  data = {
      "signInName" => account+$domain,
      "uaid"  => $config["uaid"],
      "includeSuggestions" => true,
      "uiflvr"  => $config["uiflvr"],
      "scid" => $config["scid"],
      "hpgid" => "Signup_MemberNamePage_Client",
      "tcxt" => $config["tcxt"]
  }

  
  header = {   "Cookie" => $cookie, 
               "Accept" => "application/json",
               "Accept-Encoding" => "gzip, deflate, br",
               "Accept-Language" => "en-US,en;q=0.5",
               "Connection" => "keep-alive",
               "Content-type" => "application/x-www-form-urlencoded; charset=UTF-8",
               "Host" => "signup.live.com",
               "User-Agent" => "Mozilla/5.0 (Windows NT 10.0; .) Gecko/20100101 Firefox/58.0",
               "X-Requested-With" => "XMLHttpRequest",
               "canary" => $config["apiCanary"],
               "hpgid" => "Signup_MemberNamePage_Client",
               "scid" => $config["scid"].to_s,
               "uiflvr"  => $config["uiflvr"].to_s,
               "uaid"  => $config["uaid"],
               "tcxt" => $config["tcxt"]
  }
 

  $content = ''
  $http.post(path,data.to_json,header) do |str| 
       $content += str
  end

  dCont = JSON.parse($content)
  if ( dCont.has_key? "error" ) then 
    $config["tcxt"] = dCont["error"]["telemetryContext"]
    return false
  end

  if ( dCont.has_key? "isAvailable" ) then
     $config["tcxt"] = dCont["telemetryContext"]
     $config["apiCanary"] = dCont["apiCanary"]
     return !dCont["isAvailable"]
  end
  
  return false

end

def output(line)

  pre = $alpha[rand(0..$la)]
  pos1 = $xalphan[rand(0..$lx)]
  pos2 = $xalphan[rand(0..$lx)]

  part =  "#{line}#{$domain}"

  line.gsub!(/[.]/,'')
  puts "#{pre}_#{line}#{pos1}_#{pos2},#{part}\n"
 
end


$lines = File.readlines($inputFile)

$last = ''
begin 
  $lines.each do |line|
    $last = line.chomp
    if isUsed($last) then
      output($last)
    end
    sleep(0.5)
  end

rescue Exception => e
  puts "Stopped at #{$last} because of : #{e}"
end


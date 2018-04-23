require 'net/http'
require 'json'

$inputFile = '/tmp/mt0'
$apiKey = ''
$domain = '@gmail.com'



if ARGV[0] then
  $apiKey = ARGV[0]
end

if ARGV[1] then
  $inputFile = ARGV[1]
end

if ARGV[2] then
  $domain = ARGV[2]
end


$alpha = 'abcdefghijklmnopqrstuvwzxy'
$xalphan = 'abcdefghijklmnopqrstuvwzxy0123456789'

$la = $alpha.length - 1
$lx = $xalphan.length - 1

##$http = Net::HTTP.new('api.hippoapi.com',443)
##$http.use_ssl = true
$http = Net::HTTP.new('apilayer.net',80)


def processHippo(apiKey,account)

  path = '/v3/more/json/'+apiKey+'/'+account+$domain
  header = {   
               "Accept" => "*/*",
               "Accept-Language" => "en-US,en;q=0.5",
               "Connection" => "keep-alive",
               "Content-type" => "application/json",
               "Host" => "api.hippoapi.com"
  }
  
  content = ''
  resp = $http.get(path,header) do |str|
     content += str
  end

  #puts content
  begin
     ##puts apiKey
     dCont = JSON.parse(content)
     puts dCont["hippoTrust"]["score"] 
     return (dCont["hippoTrust"]["score"] > 1)
  rescue Exception => e
     print "Error: "+content
     exit(2)
  end

end


def processMailBox(apiKey,account)

  path = '/api/check?access_key='+apiKey+'&email='+account+$domain+'&smtp=1&format=1'
  header = {
               "Accept" => "*/*",
               "Accept-Language" => "en-US,en;q=0.5",
               "Connection" => "keep-alive",
               "Content-type" => "application/json",
               "Host" => "apilayer.net"
  }

  content = ''
  resp = $http.get(path,header) do |str|
     content += str
  end

  begin
     ##puts apiKey
     dCont = JSON.parse(content)
     puts dCont["score"]
     return (dCont["score"] > 0.74)
  rescue  Exception => e
     puts "Error: "+content
     exit(2)
  end

end


def isUsed(apiKey,account)
   #return processHippo(apiKey,account)
    return processMailBox(apiKey,account)
end

=begin
#left = ("%04X" % $apiKey)
(2..8).each do |k|
  left = ("%04X" % k)
  (0..65535).each do |i|
    key = left +  ("%04X" % i)
    isUsed(key, "richard.d3")
    sleep(0.125)
  end
end
=end

def output(line)

  pre = $alpha[rand(0..$la)]
  pos1 = $xalphan[rand(0..$lx)]
  pos2 = $xalphan[rand(0..$lx)]

  part =  "#{line}#{$domain}"

  line.gsub!(/[.]/,'')
  puts "#{pre}_#{line}#{pos1}_#{pos2},#{part}\n"
 
end

=begin
    print "spencer.q7" + "\t\t"
    if isUsed($apiKey, "spencer.q7") then
      output("spencer.q7")
    end
=end

$lines = File.readlines($inputFile)

$last = ''
begin 
  $lines.each do |line|
    $last = line.chomp
    print $last + "\t\t"
    if isUsed($apiKey, $last) then
      output($last)
    end
    sleep(0.2)
  end

rescue Exception => e
  puts "Stopped at #{$last} because of : #{e}"
end

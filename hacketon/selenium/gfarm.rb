require 'net/http'


$inputFile = '/tmp/mt0'

if ARGV[0] then
  $inputFile = ARGV[0]
end

$domain = '@gmail.com'

$alpha = 'abcdefghijklmnopqrstuvwzxy'
$xalphan = 'abcdefghijklmnopqrstuvwzxy0123456789'

$la = $alpha.length - 1
$lx = $xalphan.length - 1

$http = Net::HTTP.new('accounts.google.com',443)
$http.use_ssl = true

path = '/SignUp?service=mail&continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&ltmpl=default'

resp, data = $http.get(path)

$cookie = resp["set-cookie"].split(";")[0]


def isUsed(account)
  path = '/InputValidator?resource=SignUp&service=mail'
  data = '{"Locale": "en", "input01": {"FirstName":"", "GmailAddress": "'+account+'", "Input": "GmailAddress", "LastName": ""} }' 
  header = {   "Cookie" => $cookie, 
               "Accept" => "*/*",
               "Accept-Encoding" => "gzip, deflate, br",
               "Accept-Language" => "en-US,en;q=0.5",
               "Connection" => "keep-alive",
               "Content-type" => "application/json",
               "Host" => "accounts.google.com",
               "User-Agent" => "Mozilla/5.0 (Windows NT 10.0; .) Gecko/20100101 Firefox/58.0"
  }
  
  File.open('result.gz', 'w') { |f|
  resp = $http.post(path,data,header) do |str|
     f.write str
  end
  
  $cookie = resp["set-cookie"].split(";")[0]
  }
  
  content = `zcat result.gz`
  content = content.chomp
  
  return (content =~ /"Valid"\s*:\s*"false"/)

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
    sleep(1)
  end

rescue Exception => e
  puts "Stopped at #{$last} because of : #{e}"
end


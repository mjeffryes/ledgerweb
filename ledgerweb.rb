require 'rubygems'
require 'sinatra'

get '/' do
	s = ""
	s +="<form action='/' method='get'>"
	s +="  <textarea name='result' rows='40' cols='80'>"
	IO.popen( params[:command] ){ |io|
		s += io.read
	} if params[:command]
	s +="  </textarea> <br/>"
	s +="  <input name='command' type='text'/>"
	s +="  <input type='submit'/>"
	s +="</form>" 
	return s
end

get '/balances/' do
	content_type :json
	s = ""	
	IO.popen( 'python accounts.py' ){ |io| 
		s += io.read
	}
	return s
end

get '/balances/:account' do
	content_type :json
#	s = '{"nodes":['
#	IO.popen( 'ledger bal '+ params[:account] +' --format=\'{"value":%(quantity(abs(total))), "name":"%(account)", "group":1},\n%/\' --display=\'l==2\' --flat -f drewr.dat' ){ |io|
	s = ""	
	IO.popen( "python accounts.py #{params[:account]}" ){ |io| 
		s += io.read
	}
#	s.slice!(-2)
#	s += "]}"
	
	return s
end

get '/flows/' do
	content_type :json
	s = ""	
	IO.popen("python flows.py \'#{params['accounts']}\'" ){ |io| 
		s += io.read
	}
	return s
end

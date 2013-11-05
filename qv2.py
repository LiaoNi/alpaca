import sys
import types
import datetime
import time
import MySQLdb
import math
reload(sys)
sys.setdefaultencoding('utf-8')
from selenium import webdriver
def calcnode(node):
	fl = node.find_element_by_class_name('c1')
	tm = node.find_element_by_class_name('c2')
	local = node.find_element_by_class_name('c3')
	
	fl_name = fl.find_element_by_class_name('a_name').text
	fl_model = fl.find_element_by_class_name('a_model').text
	tm_dep = tm.find_element_by_class_name('a_tm_dep').text
	tm_arv = tm.find_element_by_class_name('a_tm_arv').text
	local_dep = local.find_element_by_class_name('a_lacal_dep').text
	local_arv = local.find_element_by_class_name('a_local_arv').text

	return (fl_name,fl_model,tm_dep,tm_arv,local_dep,local_arv)

driver = webdriver.Firefox()
driver.get('http://flight.qunar.com/site/oneway_list.htm?searchDepartureAirport=%E5%8C%97%E4%BA%AC&searchArrivalAirport=%E4%B8%8A%E6%B5%B7&searchDepartureTime=2013-10-29&searchArrivalTime=2013-10-29&nextNDays=0&sd_idx=0&SearchLocation=sevenday_search');

time.sleep(20)
script = "var editPrice = function(price, pos, num) { var t = price.split(''); t[t.length - pos] = num; return t.join(''); }; var getPriceById = function(itemId) { var prices = document.getElementById(itemId).getElementsByClassName('prc')[0].getElementsByTagName('b'); var width = 0; var price = 0; for (var i = 0; i < prices.length; ++i) { if (prices[i].style.width) { width = prices[i].style.width; width = width.substring(0, width.indexOf('px')); price = prices[i].innerHTML; } else { var left = prices[i].style.left; left = Math.abs(left.substring(0, left.indexOf('px'))); price = editPrice(price, left / 11, prices[i].innerHTML); } } for (var i = prices.length - 1; i > 0; --i) { prices[i].parentNode.removeChild(prices[i]); } prices[0].innerHTML = price; return price; }; var key = new Array(); var priceArray = new Array(); var d = document.getElementById('hdivResultPanel').children; for (var i = 0; i < d.length; ++i) { key[i] = d[i].id; priceArray[i] = getPriceById(d[i].id); } "

a = 1
while  a == 1:
	try:
		driver.execute_script(script)
		result = driver.find_element_by_id('hdivResultPanel').find_elements_by_class_name('avt_column')
#conn = MySQLdb.connect(host='162.105.30.55',user='remote',passwd='alpaca',db='airTicketOnline',port=3306,charset='utf8')
#		cur = conn.cursor()
		for i in range(0,len(result)):
			today = datetime.datetime.now()
			istrans = 0
			c6 = result[i].find_element_by_class_name('c6')
			prc = c6.find_element_by_class_name('prc').text
			try:
				try:
					origin = result[i].find_element_by_class_name('b_avt_lst')	
					(fl_name,fl_model,tm_dep,tm_arv,local_dep,local_arv)=calcnode(origin)
					print fl_name+fl_model+tm_dep+tm_arv+local_dep+local_arv+prc
				except Exception as e:
					print 'trans'

				first = result[i].find_element_by_class_name('avt_column_1st')
				(fl_name,fl_model,tm_dep,tm_arv,local_dep,local_arv)=calcnode(first)
				print fl_name+fl_model+tm_dep+tm_arv+local_dep+local_arv+prc

				istrans = 1

				transcity  = result[i].find_element_by_class_name('avt_column_sp').text
				print transcity

				second = result[i].find_element_by_class_name('avt_column_2nd')
				(fl_name,fl_model,tm_dep,tm_arv,local_dep,local_arv)=calcnode(second)
				print fl_name+fl_model+tm_dep+tm_arv+local_dep+local_arv+prc
			except Exception as e:
				print 'origin';
#print e

				
			query ="insert into onlinePrice(flightNo,airplaneType,departureTime,arrivalTime,departureAirport,arrivalAirport,lowestPrice,webSource,accquiredTime) values(%s,%s,%s,%s,%s,%s,%s,'qunar.com',from_unixtime(%s))"
			value = (fl_name,fl_model,tm_dep,tm_arv,local_dep,local_arv,prc,time.mktime(today.timetuple()))
#cur.execute(query,value);
#			conn.commit()

		nextp = driver.find_element_by_id('nextXI3')
		nextp.click()
	except Exception as e:
		print e
		a = 0
		
driver.quit()



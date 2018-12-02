import requests
from lxml import html
import json
import re

#A function that fetch flight information and place it into a dictionary from air ticket booking website
def parse(triptype,origin,destination,startdate,returndate,AdultNo,bookingsite): 
	#Using regular expression to seperate date imput into parts
	  pattern=r'\d+'
	  dapartdate=re.findall(pattern,startdate)
	  enddate=re.findall(pattern,returndate)    
          
	#Formatting our url by the search criteria(including booking website)
	  if bookingsite == "1":#Fetching flight details from Expedia
	  	  for i in range(5):
	  	  	  if triptype=='1':
	  	  	  	  url = "https://www.expedia.com/Flights-Search?trip=oneway&leg1=from%3A{0}%2Cto%3A{1}%2Cdeparture%3A{2}%2F{3}%2F{4}TANYT&passengers=adults%3A{5}%2Cchildren%3A0%2Cseniors%3A0%2Cinfantinlap%3AY&options=cabinclass%3Aeconomy&mode=search&origref=www.expedia.com".format(origin,destination,dapartdate[0],dapartdate[1],dapartdate[2],AdultNo)
	  	  	  else:
	  	  	  	  url = "https://www.expedia.com/Flights-Search?flight-type=on&starDate={0}%2F{1}%2F{2}&endDate={3}%2F{4}%2F{5}&mode=search&trip=roundtrip&leg1=from%3A{6}%2Cto%3A{7}%2Cdeparture%3A{8}%2F{9}%2F{10}TANYT&leg2=from%3A{11}%2Cto%3A{12}%2Cdeparture%3A{13}%2F{14}%2F{15}TANYT&passengers=children%3A0%2Cadults%3A{16}%2Cseniors%3A0%2Cinfantinlap%3AY"\
                .format(dapartdate[0],dapartdate[1],dapartdate[2],enddate[0],enddate[1],enddate[2],origin,destination,dapartdate[0],dapartdate[1],dapartdate[2],destination,origin,enddate[0],enddate[1],enddate[2],AdultNo) 
	  else:#Fetching flight details from Orbitz
	  	  for i in range(5):
	  	  	  if triptype=='1':
	  	  	  	  url = "https://www.orbitz.com/Flights-Search?trip=oneway&leg1=from%3A{0}%2Cto%3A{1}%2Cdeparture%3A{2}%2F{3}%2F{4}TANYT&passengers=adults%3A{5}%2Cchildren%3A0%2Cseniors%3A0%2Cinfantinlap%3AY&options=cabinclass%3Aeconomy&mode=search&origref=www.orbitz.com".format(origin,destination,dapartdate[0],dapartdate[1],dapartdate[2],AdultNo)
	  	  	  else:
	  	  	  	  url = "https://www.orbitz.com/Flights-Search?flight-type=on&starDate={0}%2F{1}%2F{2}&endDate={3}%2F{4}%2F{5}&_xpid=11905%7C1&mode=search&trip=roundtrip&leg1=from%3A{6}%2Cto%3A{7}%2Cdeparture%3A{8}%2F{9}%2F{10}TANYT&leg2=from%3A{11}%2Cto%3A{12}%2Cdeparture%3A{13}%2F{14}%2F{15}TANYT&passengers=children%3A0%2Cadults%3A{16}%2Cseniors%3A0%2Cinfantinlap%3AY"\
                .format(dapartdate[0],dapartdate[1],dapartdate[2],enddate[0],enddate[1],enddate[2],origin,destination,dapartdate[0],dapartdate[1],dapartdate[2],destination,origin,enddate[0],enddate[1],enddate[2],AdultNo)	  	
	
	#Using requests library to get information using the url
	  response = requests.get(url)
	  
	#Checking to see if we successfully scrape the information
	  if not response.status_code == 200:
	  	  return None
	  try:#Using html to parse the page and save to a json file
	  	  root = html.fromstring(response.text)    
	  	  path = root.xpath("//script[@id='cachedResultsJson']//text()")
	  	  json_object =json.loads(path[0])
	  	  flight_data = json.loads(json_object["content"])
	  	  return flight_data
	  except:
	  	  return None

#A function to process the raw data
def process(flight_data,stopNo,min_price,max_price):
    lists=[]#Prepare to add info
    try:
    	  for i in flight_data['legs'].keys():
		#Select useful info from raw data for every choice
		#Price info
    		  exact_price = flight_data['legs'][i].get('price',{}).get('exactPrice','')		
    		  formatted_price = flight_data['legs'][i].get('price',{}).get('formattedPrice','')
		
		#Specific leaving and arriving time
    		  departure_time=flight_data['legs'][i].get('departureTime',{}).get('time',{})
    		  arrival_time=flight_data['legs'][i].get('arrivalTime',{}).get('time',{})
    		 
		#Departure and arrival airport codes and their location cities
    		  departure_airport_code = flight_data['legs'][i].get('departureLocation',{}).get('airportCode','')
    		  departure_city = flight_data['legs'][i].get('departureLocation',{}).get('airportCity','')
    		  arrival_airport_code = flight_data['legs'][i].get('arrivalLocation',{}).get('airportCode','')
    		  arrival_city = flight_data['legs'][i].get('arrivalLocation',{}).get('airportCity','')
    		 
		#Carrier information
    		  airline_name = flight_data['legs'][i].get('carrierSummary',{}).get('airlineName','')
    		  carrier = flight_data['legs'][i].get('timeline',[])[0].get('carrier',{})
    		  plane = carrier.get('plane','')
		
		#Duration of the flight in day/hour/minute
    		  flight_duration = flight_data['legs'][i].get('duration',{})
    		  flight_days = flight_duration.get('numOfDays','')
    		  flight_hours = flight_duration.get('hours','')
    		  flight_minutes = flight_duration.get('minutes','')
    		  
		#Format stop numbers		  
    		  num_of_stops = flight_data['legs'][i].get("stops","")		
    		  if num_of_stops==0:
    	  	  	  stop = "Nonstop"
    		  else:
    	  	  	  stop = str(num_of_stops)+' Stop'
				
		#Format time range, flight duration, departure and arrival    
    		  time_range = departure_time+'-'+arrival_time
    		  total_flight_duration = "%s days %s hours %s minutes" %(flight_days,flight_hours,flight_minutes)
    		  departure = departure_airport_code+", "+departure_city
    		  arrival = arrival_airport_code+", "+arrival_city
			
		#Format airline name			    
    		  if not airline_name:
    	  	  	  airline_name = carrier.get('operatedBy','')
			
		#Format every detailed timeline    				
    		  detailed_timelines = []
    		  for timeline in  flight_data['legs'][i].get('timeline',{}):
    	  	  	  if 'departureAirport' in timeline.keys():
    	  	  	  	  departure_airport = timeline['departureAirport'].get('longName','')
    	  	  	  	  departure_time = timeline['departureTime'].get('time','')
    	  	  	  	  arrival_airport = timeline.get('arrivalAirport',{}).get('longName','')
    	  	  	  	  arrival_time = timeline.get('arrivalTime',{}).get('time','')
    	  	  	  	  flight_timing = {
    							'time range':departure_time+'-'+arrival_time,                                  
    							'departure_airport':departure_airport,
    							'arrival_airport':arrival_airport,
    						    }
    	  	  	  	  detailed_timelines.append(flight_timing)
					
		#Combine formatted info as a dict, ready to be appended    
    		  flight_info={'ticket price':formatted_price,
    				'time range':time_range,
    				'flight duration':total_flight_duration,                    
    				'stops':stop,
    				'departure':departure,
    				'arrival':arrival,
    				'airline':airline_name,
    				'plane':plane,
    				'detailed_timelines':detailed_timelines,
    				}
			
		#Choose airticket info according to user's requirement			
    		  if int(min_price)<=int(exact_price) and int(exact_price)<=int(max_price) and num_of_stops<=int(stopNo):
    	  	  	  lists.append(flight_info)
			
	#Sort the airtickets according to ticket price
    	  sortedlist = sorted(lists, key=lambda k: k['ticket price'],reverse=False)
    	  if sortedlist == []:
            sortedlist.append("Couldn't find any flights that satisfies your criteria, please try again...")
    	  return sortedlist
    
#Capture and handle exceptions(when no result can be returned)
    except ValueError:
    	  print ("Retrying...")
    except TypeError:
    	  print ("Couldn't find any flights that satisfies your criteria, please try again...")

#Error statement
    return [{"error":"Failed to fetch data"}]

# A main function to execute the scraper
if __name__=="__main__":
	print ("Thank you for choosing our flight crawler!")
	# Allow user to enter their required triptype
	triptype=input("Please enter your trip type: 1 for oneway, 2 for roundtrip\n")
	
	# Allow user to enter the dates in date format
	pattern=r'^\d{2}/\d{2}/\d{4}$' 
	if triptype=='1':
		startdate=input("Please enter your startdate: format in MM/DD/YYYY:\n")
		if(bool(re.search(pattern, startdate))==False):
			raise ValueError('Wrong date format')            
	elif triptype=='2':       
		(startdate,returndate)=input("Please enter your startdate and returndate: format in MM/DD/YYYY\nie.12/10/2018 12/31/2018\n").split()
		if(bool(re.search(pattern, startdate)) and bool(re.search(pattern, returndate))==False):
			raise ValueError('Wrong date format') 
	else:
		raise ValueError("Wrong triptype! Please try again")
	
	# Allow user to enter the origin, destination, adult number, stop number, minimum price and maximum price
	(origin,destination)=input("Please enter your source and destination:\nie:nyc mia\n").split()
	(AdultNo,stopNo)=input("Please enter number of adults and maximum number of stops you accept:\nie:2 0\n").split()
	(min_price,max_price)=input("Please enter the price range:min max\nie:200 300\n").split()

	# Allow user to choose the booking site
	(bookingsite)=input("Please enter your desired booking website: 1 for Expedia, 2 for Orbitz\n")
	if not (bookingsite=='1' or bookingsite=='2'):
		raise ValueError('Wrong booking site! Please try again')
	
    	# Execution of the crawler
	print ("Fetching flight details")
	if triptype=='1':
		scraped_data = process(parse(triptype, origin, destination, startdate, '00/00/0000', AdultNo, bookingsite), stopNo, min_price, max_price)
	else:
 		scraped_data = process(parse(triptype, origin, destination, startdate, returndate, AdultNo, bookingsite), stopNo, min_price, max_price)       	
	
	# Write the selected json data to a file
	print ("Writing data to output file...")
	with open('Your-flight-results-%s-%s.json'%(origin, destination),'w') as fp:
		json.dump(scraped_data,fp,indent = 4)

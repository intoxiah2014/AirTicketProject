import requests
from lxml import html
import json
import re

def parse(triptype,source,destination,startdate,returndate,AdultNo):
	  pattern=r'\d+'
	  dapartdate=re.findall(pattern,startdate)
	  enddate=re.findall(pattern,returndate)    
	  for i in range(5):
	  	  if triptype=='oneway':
	  	  	  url = "https://www.expedia.com/Flights-Search?trip=oneway&leg1=from%3A{0}%2Cto%3A{1}%2Cdeparture%3A{2}%2F{3}%2F{4}TANYT&passengers=adults%3A{5}%2Cchildren%3A0%2Cseniors%3A0%2Cinfantinlap%3AY&options=cabinclass%3Aeconomy&mode=search&origref=www.expedia.com".format(source,destination,dapartdate[0],dapartdate[1],dapartdate[2],AdultNo)
	  	  elif triptype=='roundtrip':
	  	  	  url="https://www.expedia.com/Flights-Search?flight-type=on&starDate={0}%2F{1}%2F{2}&endDate={3}%2F{4}%2F{5}&mode=search&trip=roundtrip&leg1=from%3A{6}%2Cto%3A{7}%2Cdeparture%3A{8}%2F{9}%2F{10}TANYT&leg2=from%3A{11}%2Cto%3A{12}%2Cdeparture%3A{13}%2F{14}%2F{15}TANYT&passengers=children%3A0%2Cadults%3A{16}%2Cseniors%3A0%2Cinfantinlap%3AY"\
                .format(dapartdate[0],dapartdate[1],dapartdate[2],enddate[0],enddate[1],enddate[2],source,destination,dapartdate[0],dapartdate[1],dapartdate[2],destination,source,enddate[0],enddate[1],enddate[2],AdultNo)
	  	  else:
	  	  	  raise ValueError('wrong input') 
	  response = requests.get(url)
	  if not response.status_code == 200:
	  	  return None
	  try:
	  	  root = html.fromstring(response.text)    
	  	  path = root.xpath("//script[@id='cachedResultsJson']//text()")
	  	  json_object =json.loads(path[0])
	  	  flight_data = json.loads(json_object["content"])
	  	  return flight_data
	  except:
	  	  return None

def process(flight_data,stopNo,min_price,max_price):
    lists=[]
    try:
    	  for i in flight_data['legs'].keys():
    		  formatted_price = flight_data['legs'][i].get('price',{}).get('formattedPrice','')
    	  	  departure_location_airport = flight_data['legs'][i].get('departureLocation',{}).get('airportLongName','')
    	  	  departure_location_city = flight_data['legs'][i].get('departureLocation',{}).get('airportCity','')
    	  	  arrival_location_airport = flight_data['legs'][i].get('arrivalLocation',{}).get('airportLongName','')
    	  	  arrival_location_city = flight_data['legs'][i].get('arrivalLocation',{}).get('airportCity','')
    	  	  airline_name = flight_data['legs'][i].get('carrierSummary',{}).get('airlineName','')
    				
    	  	  no_of_stops = flight_data['legs'][i].get("stops","")
    	  	  flight_duration = flight_data['legs'][i].get('duration',{})
    	  	  flight_hour = flight_duration.get('hours','')
    	  	  flight_minutes = flight_duration.get('minutes','')
    	  	  flight_days = flight_duration.get('numOfDays','')
    
    	  	  if no_of_stops==0:
    	  	  	  stop = "Nonstop"
    	  	  else:
    	  	  	  stop = str(no_of_stops)+' Stop'
    
    	  	  total_flight_duration = "%s days %s hours %s minutes" % flight_days,flight_hour,flight_minutes
    	  	  departure = departure_location_airport+", "+departure_location_city
    	  	  arrival = arrival_location_airport+", "+arrival_location_city
    	  	  carrier = flight_data['legs'][i].get('timeline',[])[0].get('carrier',{})
    	  	  plane = carrier.get('plane','')
    	  	  plane_code = carrier.get('planeCode','')
    
    	  	  if not airline_name:
    	  	  	  airline_name = carrier.get('operatedBy','')
    				
    	  	  timings = []
    	  	  for timeline in  flight_data['legs'][i].get('timeline',{}):
    	  	  	  if 'departureAirport' in timeline.keys():
    	  	  	  	  departure_airport = timeline['departureAirport'].get('longName','')
    	  	  	  	  departure_time = timeline['departureTime'].get('time','')
    	  	  	  	  arrival_airport = timeline.get('arrivalAirport',{}).get('longName','')
    	  	  	  	  arrival_time = timeline.get('arrivalTime',{}).get('time','')
    	  	  	  	  flight_timing = {
    											'departure_airport':departure_airport,
    											'departure_time':departure_time,
    											'arrival_airport':arrival_airport,
    											'arrival_time':arrival_time
    						    }
    	  	  	  	  timings.append(flight_timing)
    
    	  	  flight_info={'stops':stop,
    				'ticket price':formatted_price,
    				'departure':departure,
    				'arrival':arrival,
    				'flight duration':total_flight_duration,
    				'airline':airline_name,
    				'plane':plane,
    				'timings':timings,
    				'plane code':plane_code
    				}
    	  	  if int(min_price)<=int(exact_price) and int(exact_price)<=int(max_price) and no_of_stops<=int(stopNo):
    	  	  	  lists.append(flight_info)
    	  sortedlist = sorted(lists, key=lambda k: k['ticket price'],reverse=False)
    	  return sortedlist
		
    except ValueError:
    	  print ("Rerying...")
			
    return [{"error":"failed to process the page"}]

# a main function to execute the scraper, however did not figure out how to execute the process function
if __name__=="__main__":
	argparser = argparse.ArgumentParser()
	argparser.add_argument('source',help = 'Source airport code')
	argparser.add_argument('destination',help = 'Destination airport code')
	argparser.add_argument('startdate',help = 'MM/DD/YYYY')
	argparser.add_argument('returndate',help = 'MM/DD/YYYY')
	argparser.add_argument('triptype', help = '"oneway" or "roundtrip"')
	argparser.add_argument('stopNo', help = 'Number of Stops')
	argparser.add_argument('max_price',help = 'Maximum Price')
	argparser.add_argument('min_price',help = 'Minimum Price')
	argparser.add_argument('AdultNo',help = 'Number of Adults')
    

	args = argparser.parse_args()
	source = args.source
	destination = args.destination
	startdate = args.startdate
	returndate = args.returndate
	triptype = args.triptype
	stopNo = args.stopNo
	max_price = args.max_price
	min_price = args.min_price
	AdultNo = args.AdultNo
    
	print ("Fetching flight details")
	scraped_data = process(parse(triptype, source, destination, startdate, returndate, AdultNo), stopNo, min_price, max_price)
	print ("Writing data to output file")
	with open('%s-%s-flight-results.json'%(source, destination),'w') as fp:
	 	json.dump(scraped_data,fp,indent = 4)


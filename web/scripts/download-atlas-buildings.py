"""Download the official whole-Berlin geometry with deterministic WFS pagination.

Usage: python3 web/scripts/download-atlas-buildings.py /tmp/berlin-city
Only public numeric geometry is requested. Raw exports stay outside the site.
"""
import urllib.request,urllib.parse,json,pathlib,time,concurrent.futures,sys
import xml.etree.ElementTree as ET
out=pathlib.Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=True)
base='https://gdi.berlin.de/services/wfs/ua_gebaeudehoehen'
params=dict(service='WFS',version='2.0.0',request='GetFeature',typeNames='ua_gebaeudehoehen:gebaeudehoehen',outputFormat='application/json',propertyName='geom,hoehe,shape_area,gisid',count='100000',sortBy='gisid')
hits={k:v for k,v in params.items() if k != 'outputFormat'}|{'resultType':'hits'}
request=urllib.request.Request(base+'?'+urllib.parse.urlencode(hits),headers={'User-Agent':'Mozilla/5.0 Berlin atlas public geodata export'})
total=int(ET.fromstring(urllib.request.urlopen(request,timeout=60).read()).attrib['numberMatched'])
def page(start):
 p=out/f'buildings-{start:07}.json'
 if p.exists():
  cached=json.loads(p.read_bytes())
  if cached.get('numberMatched')==total and len(cached.get('features',[]))==min(100000,total-start):return str(p)
  raise ValueError('Existing page belongs to a different export; use an empty output directory')
 q=params|{'startIndex':str(start)}
 for attempt in range(3):
  try:
   req=urllib.request.Request(base+'?'+urllib.parse.urlencode(q),headers={'User-Agent':'Mozilla/5.0 Berlin atlas public geodata export'})
   raw=urllib.request.urlopen(req,timeout=240).read(); data=json.loads(raw)
   expected=min(100000,total-start)
   if len(data['features'])!=expected or data['numberMatched']!=total:raise ValueError('Incomplete or changed source')
   p.write_bytes(raw);print(p.name,len(raw),len(data['features']),flush=True);return str(p)
  except Exception:
   if attempt==2:raise
   time.sleep(2)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(page,range(0,total,100000)))
print(f'All {total} source features downloaded',flush=True)

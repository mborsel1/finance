import time
import urllib2
from urllib2 import urlopen

russell3000 = []
NCAVstocks = []
NCAVbad = ['ACW', 'AKS', 'ATI', 'CRMT', 'AXE', 'AHP', 'AHT', 'AINC', 'AAVL', 'BAS', 'BBOX', 'CAB', 'CSLT', 'CDI', 'CCS', 'CCO', 'CIE', 'CMC', 'CVGI', 'CYH', 'CONN', 'CMLS', 'DCO', 'KODK', 'SATS', 'RDEN', 'ECYT', 'EXXI', 'ENVA', 'EVLV', 'EZPW', 'FDML', 'F', 'FSTR', 'FTR', 'BGC', 'GEN', 'GNCA', 'GEOS', 'HLX', 'HOS', 'IMN', 'IO', 'JAKK', 'JONE', 'JOY', 'KEG', 'KLXI', 'LUK', 'LCUT', 'VAC', 'MLNK', 'MRC', 'NAV', 'NWPX', 'NRG', 'ZEUS', 'PKOH', 'PKD', 'PSIX', 'PRAA', 'RTK', 'RYI', 'SGMS', 'SALT', 'SENEA', 'SSE', 'SZMK', 'SKUL', 'SSI', 'TESO', 'TTPH', 'TDW', 'TLYS', 'TWI', 'TITN', 'TGI', 'TROX', 'TPC', 'X', 'UVV', 'VHI', 'VSTM', 'VRTV', 'VC', 'VVUS', 'WMAR', 'ZFGN', 'ZAIS', 'GURE']

NCAVbetter = []
shortlist = []
shortdict = {}
divlist = []

def parseRus():
	try:
		readFile = open('russell3000.txt','r').read()
		splitFile = readFile.split('\n')
		for eachLine in splitFile:
			splitLine = eachLine.split(' ')
			ticker = splitLine[-1]
			russell3000.append(ticker)
		#print russell3000
		
	except Exception, e:
		print 'failed in the main loop', str(e)

#parseRus()


def netCurrent(stock):

	
	sourceCode = urllib2.urlopen("https://finance.yahoo.com/q/bs?s="+stock).read()
	sourceCode2 = urllib2.urlopen("https://finance.yahoo.com/q/ks?s="+stock+"+Key+Statistics").read()
	
	try:
		price = float(sourceCode.split('<span class="time_rtq_ticker"><span id="yfs_l84_'+stock.lower()+'">')[1].split('</span>')[0])
	
		assets = sourceCode.split("""Total Current Assets
                            </strong>
                        </td><td align="right">
                                <strong>
                            """)[1].split('&nbsp;&nbsp;')[0]
		ass1 = assets.replace(",","")
		
		cliab = sourceCode.split("""Total Current Liabilities
                            </strong>
                        </td><td align="right">
                                <strong>
                            """)[1].split('&nbsp;&nbsp;')[0]
		cliab1 = cliab.replace(",","")
	
		tliab = sourceCode.split("""Total Liabilities
                            </strong>
                        </td><td align="right">
                                <strong>
                            """)[1].split('&nbsp;&nbsp;')[0]
		tliab1 = tliab.replace(",","")
	
		shares = sourceCode2.split('Shares Outstanding<font size="-1"><sup>5</sup></font>:</td><td class="yfnc_tabledata1">')[1].split('</td>')[0]
		if shares.endswith('B'):
			share1 = shares.replace("B","")
			sharesOut = int(float(share1)*1000000000)
		elif shares.endswith('M'):
			share1 = shares.replace("M","")
			sharesOut = int(float(share1)*1000000)
	
		currentAssets = int(float(ass1)*1000)
		currentLiab = int(float(cliab1)*1000)
		totalLiab = int(float(tliab1)*1000)
		NCAV = float((currentAssets-totalLiab)/sharesOut)
	
		if NCAV/price > 1:
			NCAVstocks.append(stock)
		else:
			pass
		if NCAV/price > 1 and currentAssets/currentLiab > 2:
			NCAVbetter.append(stock)
		else:
			pass
			#print "-" * 40
			#print ""
			#print stock, "has a NCAV/share of: ", NCAV/price
			#print ""
		#else:
			#print stock,"failed"
	
	except Exception, e:
		print stock, "failed with exception"

	print NCAVstocks
	print NCAVbetter
	
		
		
def screener(stock):
	
	sourceCode = urllib2.urlopen("https://finance.yahoo.com/q?s="+stock).read()
	sourceCode2 = urllib2.urlopen("https://finance.yahoo.com/q/ks?s="+stock+"+Key+Statistics").read()

	try:
		price = float(sourceCode2.split('<span class="time_rtq_ticker"><span id="yfs_l84_'+stock.lower()+'">')[1].split('</span>')[0])
		#print price
		
		eps = float(sourceCode.split('EPS <span class="small">(ttm)</span>:</th><td class="yfnc_tabledata1">')[1].split('</td>')[0])
		#print eps
		
		bvps = float(sourceCode2.split('Book Value Per Share (mrq):</td><td class="yfnc_tabledata1">')[1].split('</td>')[0])
		#print bvps
		
		if eps > 0:
			graham = math.sqrt(22.5 * eps * bvps)
			if graham > 0:
				shortlist.append(stock)
				shortdict.update({stock:graham-price})
				print "-"*30
				print ""
				print stock
				print "price:", price
				print "graham:", graham
				print "graham - price:", graham-price
				print "eps:", eps
				print "bvps:", bvps
				#try:
					#div = float(sourceCode2.split('Div &amp; Yield:</th><td class="yfnc_tabledata1">')[1].split(' (')[0])
					#if div > 0:
						#divlist.append(stock)
						#print "div:", div
					#else:
						#pass
				#except Exception, e:
					#pass
				if price/bvps >1.5:
					print "red flag, price vs bvps problem"
					print price/bvps
				else:
					pass
			else:
				pass

		else:
			print "-"*30
			print stock, "ineligible"
	
	except Exception, e:
		print stock, "exception"


	
for eachStock in NCAVbad:
	netCurrent(eachStock)
	#time.sleep(2)
	






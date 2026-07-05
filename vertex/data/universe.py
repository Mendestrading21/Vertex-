"""
vertex/data/universe.py — L'UNIVERS de VERTEX (données pures, aucune logique).

Listes de tickers scannés, ensembles d'indices (Dow/Nasdaq/S&P/Russell/EU/Asia),
cartographie ticker→secteur GICS et ticker→industrie. Extrait de terminal.py
(refonte institutionnelle — responsabilité unique : la donnée d'univers).
"""

WATCHLIST = ['AAPL', 'NVDA', 'MSFT', 'META', 'GOOGL', 'AMZN', 'AVGO', 'TSLA',
             'NFLX', 'AMD', 'CRM', 'COST', 'LLY', 'JPM', 'V', 'MA', 'HD',
             'UNH', 'XOM', 'WMT', 'PLTR', 'NOW', 'TSM', 'ASML', 'ANET', 'MU',
             'QCOM', 'ARM', 'SMCI', 'PANW', 'SNOW', 'CRWD', 'UBER', 'ABNB',
             'SHOP', 'COIN', 'MSTR', 'INTU', 'ORCL', 'ADBE', 'AMAT', 'MRVL',
             'DELL', 'CEG', 'VRT',
             # momentum / « qui cartonnent » (MAJ 26.06.2026) : AI infra, power, fintech, adtech, connectivité IA
             'HOOD', 'AXON', 'NET', 'MELI', 'RDDT', 'APP', 'ISRG',
             'GEV', 'VST', 'ALAB', 'CRDO', 'NBIS']
# ─── UNIVERS ÉLARGI : ~110 plus grosses capitalisations US (S&P 500 / Nasdaq / Dow) ───
# scanné automatiquement (cockpit, watchlist). Le streaming IBKR live, les news et les
# fondamentaux restent sur le core WATCHLIST (57) → limites IBKR + perfs respectées.
_BIG_EXTRA = [
    'BRK-B', 'JNJ', 'PG', 'KO', 'PEP', 'ABBV', 'MRK', 'TMO', 'ABT', 'DHR', 'PFE', 'BMY',
    'AMGN', 'GILD', 'VRTX', 'CVS', 'MDT',
    'BAC', 'WFC', 'GS', 'MS', 'C', 'AXP', 'SCHW', 'BLK', 'SPGI', 'CB', 'PGR', 'BX',
    'CSCO', 'IBM', 'INTC', 'TXN', 'ADI', 'LRCX', 'KLAC', 'MCHP', 'NXPI',
    'DIS', 'CMCSA', 'T', 'VZ', 'TMUS',
    'CAT', 'BA', 'HON', 'GE', 'RTX', 'LMT', 'DE', 'MMM', 'UPS', 'ETN',
    'CVX', 'COP', 'SLB',
    'MCD', 'NKE', 'SBUX', 'LOW', 'TJX', 'BKNG', 'PM', 'MO',
    'GM', 'F', 'PYPL', 'LIN', 'ACN', 'TXT',
]
# ─── VALEURS « TREND » : celles qui font le buzz / momentum / fast movers ───
# IA & quantum, nucléaire/énergie IA, crypto-mining, fintech, EV, meme stocks,
# espace/défense, IPO chaudes. Très volatiles — pour repérer ce qui bouge.
_TREND_EXTRA = [
    'SOFI', 'AFRM', 'UPST', 'DKNG', 'RBLX', 'U', 'PINS', 'SNAP', 'LYFT',
    'RIVN', 'LCID', 'NIO', 'GME', 'BABA', 'NU', 'GRAB',
    'MARA', 'RIOT', 'CLSK', 'WULF', 'CIFR',
    'IONQ', 'RGTI', 'QBTS', 'SOUN', 'BBAI', 'AI', 'PATH', 'DDOG', 'ZS', 'TTD',
    'HIMS', 'TEM', 'CRWV', 'CART', 'CAVA', 'DJT',
    'RKLB', 'OKLO', 'SMR', 'LUNR', 'ACHR', 'JOBY',
    'PLUG', 'FSLR', 'ENPH', 'RUN', 'DASH', 'ROKU', 'ABNB',
]
# ─── UNIVERS LARGE ~500 : reste du S&P 500 + grosses mid-caps liquides (tous secteurs) ───
# Scanné/scoré comme le reste. IBKR live + news restent sur le core (limites IBKR) ;
# le chargeur yfinance est par lots robustes → un ticker invalide/délisté est simplement ignoré.
_SP500_EXTRA = [
    # tech / semis / hardware
    'MPWR','ON','SWKS','TER','ENTG','QRVO','WDC','STX','HPQ','HPE','NTAP','JNPR','FFIV','AKAM',
    'GEN','ZBRA','TRMB','PTC','ANSS','CDNS','SNPS','FTNT','GDDY','VRSN','CTSH','IT','GLW','APH','TEL','KEYS',
    'WDAY','TEAM','OKTA','HUBS','MDB','TWLO','GTLB','S','ESTC','ZM','DOCU',
    # internet / media
    'WBD','PARA','FOXA','FOX','NWSA','OMC','IPG','LYV','EA','TTWO','MTCH','SPOT','PDD','JD','BIDU','SE',
    # financials
    'USB','PNC','TFC','COF','BK','STT','FITB','MTB','HBAN','RF','KEY','CFG','ALLY','SYF','DFS',
    'ICE','CME','MCO','MSCI','NDAQ','CBOE','AON','MMC','AJG','MET','PRU','AFL','ALL','TRV','HIG','AIG','ACGL','WTW',
    # healthcare
    'ELV','CI','HUM','CNC','MOH','SYK','BSX','EW','ZBH','BDX','BAX','HCA','MCK','COR','CAH','ZTS',
    'IDXX','IQV','A','DGX','LH','RMD','ALGN','MTD','WST','BIIB','REGN','MRNA','ILMN','INCY','RVTY',
    # consumer
    'TGT','DG','DLTR','ROST','KR','SYY','KMB','CL','GIS','K','HSY','MDLZ','KHC','STZ','KDP','MNST','KVUE',
    'CLX','CHD','EL','ULTA','LULU','YUM','CMG','DRI','MAR','HLT','RCL','CCL','NCLH','EXPE','DPZ',
    'ORLY','AZO','GPC','BBY','TSCO','DKS',
    # industrials
    'EMR','ITW','PH','ROP','CMI','PCAR','NSC','UNP','CSX','FDX','ODFL','JBHT','CHRW','WM','RSG','PWR',
    'AME','ROK','DOV','FTV','IR','XYL','PNR','GNRC','HUBB','URI','FAST','GWW','PAYX','ADP','BR','JKHY','FI','GPN',
    # energy
    'EOG','MPC','PSX','VLO','OXY','WMB','KMI','OKE','HAL','BKR','DVN','FANG','HES','TRGP','LNG','CTRA','EQT',
    # materials
    'APD','SHW','ECL','FCX','NEM','NUE','STLD','DOW','DD','PPG','VMC','MLM','ALB','CF','MOS','IFF','CTVA',
    # utilities
    'NEE','DUK','SO','D','AEP','EXC','XEL','SRE','PCG','ED','WEC','ES','PEG','AEE','DTE','FE','ETR',
    # real estate
    'PLD','AMT','EQIX','CCI','PSA','O','SPG','WELL','DLR','VICI','AVB','EQR','SBAC','EXR',
]
# ─── UNIVERS XXL (~1000) : reste du Russell 1000 + mid/small caps US très suivies ───
# Scoré comme le reste. Le chargeur yfinance par lots ignore tout ticker invalide/délisté.
# ⚠️ Scan plus long (~2-4 min) mais sous le cycle de 5 min ; IBKR live reste borné aux abos.
_RUSSELL_EXTRA = [
    # software / cloud / fintech
    'ADSK','FICO','TYL','MANH','PCTY','PAYC','DAY','WIX','APPF','BL','BLKB','FOUR','FLYW','TOST',
    'ALRM','CWAN','DLO','DOCN','FRSH','GWRE','JAMF','NCNO','PD','PGNY','QTWO','RNG','RPD','SMAR',
    'SPSC','SQSP','VERX','WK','ZUO','BIGC','BRZE','CXM','EGHT','EXLS','FSLY','INFA','KVYO','MQ',
    'RAMP','RXT','SABR','VRNS','VRNT','ZETA','AI','BBAI','SOUN','PLTR','GTLB','S','ESTC','CFLT',
    'PATH','U','ASAN','MNDY','PCOR','BSY','DBX','BOX','YEXT','DOMO','AVPT','BTDR',
    # semis / hardware
    'AMKR','AEIS','ACLS','CRUS','DIOD','FORM','HIMX','ICHR','IDCC','INDI','KLIC','LSCC','MTSI',
    'NVMI','NVTS','PLAB','POWI','RMBS','SITM','SLAB','SMTC','SYNA','UCTT','VECO','WOLF','AMBA',
    'COHR','CIEN','LITE','VIAV','INFN','ASTS','AAOI','CAMT','OLED','ALGM','SGH','PI',
    # biotech / pharma
    'ACAD','ALKS','ALNY','AMPH','APLS','ARWR','AXSM','BCRX','BHVN','BMRN','BPMC','CRSP','CYTK',
    'DVAX','EXEL','FOLD','HALO','INSM','IONS','ITCI','JAZZ','KRTX','KYMR','LGND','MDGL','MRUS',
    'NBIX','NTLA','NUVL','PCVX','PTCT','RARE','RCKT','RGNX','RYTM','SRPT','SWTX','TGTX','UTHR',
    'VKTX','XNCR','ARVN','BEAM','DNLI','EDIT','FATE','RXRX','SANA','VERV','CGEM','KROS','VCEL',
    # health services / devices
    'TECH','NTRA','EXAS','GH','NVST','PEN','PODD','TNDM','INSP','SHC','GMED','ICUI','ITGR','LIVN',
    'MASI','NARI','OMCL','TMDX','AXNX','CRVL','EVH','HQY','OSCR','PRVA','RDNT','TDOC','ACHC','AMED',
    'CHE','DOCS','EHC','ENSG','HSIC','OPCH','PINC','SEM','USPH','HIMS',
    # financials / banks / insurance
    'AMP','BEN','BRO','CINF','CNA','ERIE','FNF','GL','IVZ','JHG','KMPR','L','LNC','MKL','MKTX',
    'ORI','PFG','PRI','RGA','RJF','RLI','RNR','SF','SLM','THG','TROW','UNM','VOYA','WRB','ZION',
    'AGNC','NLY','STWD','RITM','OZK','PB','WAL','WBS','EWBC','CADE','CMA','FHN','SNV','ASB','BPOP',
    'COLB','FULT','ONB','PNFP','SSB','UMBF','VLY','WTFC','AX','FFIN','GBCI','HOMB',
    # consumer / retail / restaurants / travel
    'AAP','ANF','BBWI','BOOT','BURL','CHWY','CROX','CVNA','DECK','FIVE','FL','GPS','GES','JWN',
    'KSS','LEVI','SIG','SKX','TPR','URBN','VFC','WSM','W','YETI','CASY','COKE','BJ','PSMT','SFM',
    'ACI','GO','BLMN','BROS','CAKE','EAT','JACK','PZZA','SHAK','TXRH','WEN','WING','SG','PTLO',
    'CHH','H','TRIP','TNL','WH','MGM','LVS','WYNN','CZR','PENN','BYD','RSI','GENI','PLNT','EYE',
    # industrials / transport / aero
    'AAL','UAL','DAL','LUV','ALK','JBLU','ATI','BWXT','CW','HEI','HII','HWM','KTOS','LDOS','SPR',
    'TDG','TDY','WWD','ACM','AGX','AIT','ALLE','AOS','APG','AYI','BLDR','BLD','CARR','CSL','CR',
    'DCI','EME','ENS','FBIN','FELE','GGG','GTES','IEX','JBT','KAI','LII','MAS','MIDD','MSA','NDSN',
    'NPO','NVT','OTIS','PRIM','RRX','SPXC','SSD','TKR','TT','TREX','VMI','WAB','WCC','WTS','XPO',
    'GXO','EXPD','HUBG','KNX','LSTR','MATX','SAIA','SNDR','WERN','ARCB','PCAR',
    # energy
    'AR','BTU','CNX','CHRD','CIVI','CRK','DINO','GPOR','HP','KOS','MGY','MTDR','MUR','NOG','OVV',
    'PR','PTEN','RRC','SM','SWN','VNOM','CRGY','CHX','FTI','HLX','LBRT','NBR','OII','PUMP','RES',
    'WFRD','NOV','CLB','TS','GLNG','NFG','SWX','SR','NJR','NWN','OGS','AWR','MSEX','WTRG','AWK',
    # materials
    'ASH','AVNT','AXTA','CBT','CC','CE','EMN','FUL','HUN','KRO','KWR','LYB','OLN','RPM','SCL',
    'SXT','TROX','WLK','AA','CENX','CMC','CLF','RS','X','MP','AEM','AU','BTG','CDE','EGO','FNV',
    'GFI','GOLD','HL','IAG','KGC','NGD','PAAS','SBSW','SSRM','WPM','AG','FSM',
    # utilities / REITs
    'LNT','NI','OGE','PNW','EVRG','IDA','NWE','PNM','AVA','BKH','ADC','AMH','BRX','BXP','CPT',
    'CTRE','CUBE','CUZ','DEI','DOC','ELS','ESS','FRT','GLPI','HIW','HR','HST','IRT','KIM','KRC',
    'LAMR','MAC','NHI','NNN','NSA','OHI','PECO','REG','REXR','RHP','ROIC','SLG','STAG','SUI','TRNO',
    'UDR','UE','WPC','EPR','FCPT','IRM','MPW','PK','BNL','EPRT','SAFE','SVC','UNIT','VICI',
    # comms / media / internet
    'WBD','PARA','FOXA','FOX','NWSA','OMC','IPG','LYV','EA','TTWO','MTCH','SPOT','PINS','SNAP',
    'BIDU','JD','SE','RDDT','DASH','LYFT','ROKU','FUBO','CHTR','LBRDK','LILA','MSGS','NYT','WMG',
    'IQ','BILI','GRPN','YELP','TRIP','CARG','CARS','EVER','QNST','ZD',
]
# ─── ETF SECTORIELS SPDR (XL*) : rotation sectorielle en direct ───
_SECTOR_ETFS = ['XLK', 'XLF', 'XLE', 'XLV', 'XLI', 'XLY', 'XLP', 'XLU', 'XLB', 'XLRE', 'XLC']
# ─── GRANDES CAPS EUROPE (suffixes yfinance : .PA .DE .SW .L .MC .MI .AS .CO) ───
_EUROPE = ['ASML.AS', 'PRX.AS', 'MC.PA', 'OR.PA', 'TTE.PA', 'SAN.PA', 'AIR.PA', 'RMS.PA', 'SU.PA',
           'BNP.PA', 'AI.PA', 'DG.PA', 'EL.PA', 'SAP.DE', 'SIE.DE', 'ALV.DE', 'DTE.DE', 'BAS.DE',
           'MBG.DE', 'BMW.DE', 'ADS.DE', 'DHL.DE', 'MUV2.DE', 'IFX.DE', 'NESN.SW', 'NOVN.SW', 'ROG.SW',
           'ZURN.SW', 'UBSG.SW', 'AZN.L', 'SHEL.L', 'HSBA.L', 'ULVR.L', 'BP.L', 'GSK.L', 'RIO.L',
           'DGE.L', 'IBE.MC', 'SAN.MC', 'ITX.MC', 'ENEL.MI', 'ISP.MI', 'UCG.MI', 'RACE.MI', 'NOVO-B.CO']
# ─── GRANDES CAPS ASIE (Tokyo .T · Hong Kong .HK · Corée .KS · Taïwan .TW) ───
_ASIA = ['7203.T', '6758.T', '9984.T', '8306.T', '6861.T', '9432.T', '6098.T', '7974.T', '8035.T',
         '4063.T', '9433.T', '6501.T', '7267.T', '8058.T', '9983.T', '0700.HK', '9988.HK', '3690.HK',
         '1299.HK', '0941.HK', '1810.HK', '2318.HK', '0388.HK', '1211.HK', '005930.KS', '000660.KS',
         '005380.KS', '051910.KS', '2330.TW', '2317.TW', '2454.TW']
UNIVERSE = list(dict.fromkeys(WATCHLIST + _BIG_EXTRA + _TREND_EXTRA + _SP500_EXTRA + _RUSSELL_EXTRA + _SECTOR_ETFS + _EUROPE + _ASIA))   # dédupliqué

# ─── APPARTENANCE AUX INDICES (pour « top Dow / Nasdaq / S&P ») ───
_DOW30 = ['AAPL', 'AMGN', 'AMZN', 'AXP', 'BA', 'CAT', 'CRM', 'CSCO', 'CVX', 'DIS', 'GS', 'HD',
          'HON', 'IBM', 'JNJ', 'JPM', 'KO', 'MCD', 'MMM', 'MRK', 'MSFT', 'NKE', 'NVDA', 'PG',
          'SHW', 'TRV', 'UNH', 'V', 'VZ', 'WMT']
_NDX100 = ['AAPL', 'MSFT', 'NVDA', 'AMZN', 'META', 'GOOGL', 'GOOG', 'AVGO', 'TSLA', 'COST', 'NFLX',
           'AMD', 'PEP', 'TMUS', 'CSCO', 'ADBE', 'LIN', 'TXN', 'QCOM', 'INTC', 'AMAT', 'INTU', 'ISRG',
           'CMCSA', 'AMGN', 'HON', 'BKNG', 'VRTX', 'ADP', 'REGN', 'MU', 'PANW', 'LRCX', 'ADI', 'GILD',
           'SBUX', 'MELI', 'KLAC', 'SNPS', 'CDNS', 'CRWD', 'MDLZ', 'PYPL', 'MAR', 'ORLY', 'CTAS',
           'ABNB', 'NXPI', 'MRVL', 'FTNT', 'DASH', 'ADSK', 'WDAY', 'ROP', 'PCAR', 'MNST', 'CPRT',
           'PAYX', 'KDP', 'ODFL', 'ROST', 'CHTR', 'AEP', 'FANG', 'KHC', 'EA', 'FAST', 'CTSH', 'DDOG',
           'VRSK', 'EXC', 'GEHC', 'BKR', 'XEL', 'TTWO', 'CSGP', 'IDXX', 'ANSS', 'ON', 'MCHP', 'ZS',
           'DXCM', 'CDW', 'TEAM', 'WBD', 'MDB', 'LULU', 'TTD', 'ARM', 'SMCI', 'MRNA', 'BIIB', 'GFS', 'CCEP']
_SP500_SET = list(dict.fromkeys(
    ['AAPL', 'NVDA', 'MSFT', 'META', 'GOOGL', 'GOOG', 'AMZN', 'AVGO', 'TSLA', 'NFLX', 'AMD', 'CRM',
     'COST', 'LLY', 'JPM', 'V', 'MA', 'HD', 'UNH', 'XOM', 'WMT', 'NOW', 'ORCL', 'ADBE', 'AMAT',
     'MRVL', 'QCOM', 'PANW', 'INTU', 'DELL', 'CEG', 'VST', 'ISRG', 'GEV', 'MU', 'UBER', 'ABNB', 'SMCI']
    + _BIG_EXTRA + _SP500_EXTRA))
_RUT_SET = list(dict.fromkeys(_RUSSELL_EXTRA))   # small caps US ≈ Russell 2000

# ─── CLASSIFICATION SECTORIELLE GICS STATIQUE (page Secteurs) ───
# Mapping ticker→secteur GICS FIABLE (indépendant de yfinance/fondamentaux, jamais
# throttlé) → chaque secteur a ≥10 sociétés en direct. Utilisé pour la vue Secteurs.
_GICS = {
    'Technology': ['AAPL', 'MSFT', 'NVDA', 'AVGO', 'ORCL', 'CRM', 'AMD', 'ADBE', 'ACN', 'CSCO', 'NOW',
        'IBM', 'QCOM', 'TXN', 'INTU', 'AMAT', 'MU', 'ADI', 'LRCX', 'KLAC', 'PANW', 'CRWD', 'SNPS', 'CDNS',
        'MRVL', 'ANET', 'DELL', 'NXPI', 'MCHP', 'FTNT', 'ROP', 'ADSK', 'MPWR', 'ON', 'SMCI', 'HPQ', 'HPE',
        'WDAY', 'TEAM', 'SNOW', 'NET', 'DDOG', 'ZS', 'PLTR', 'APP', 'ARM', 'TSM', 'ASML', 'INTC', 'CTSH',
        'GLW', 'STX', 'WDC', 'TER', 'ENPH', 'FSLR', 'GFS', 'ANSS', 'CDW', 'KEYS', 'TYL', 'PTC', 'CRDO', 'ALAB'],
    'Financial Services': ['BRK-B', 'JPM', 'V', 'MA', 'BAC', 'WFC', 'GS', 'MS', 'AXP', 'BLK', 'SCHW', 'C',
        'SPGI', 'CB', 'PGR', 'MMC', 'ICE', 'CME', 'PNC', 'USB', 'TFC', 'COF', 'BK', 'AON', 'MCO', 'AJG',
        'AIG', 'MET', 'PRU', 'AFL', 'ALL', 'TRV', 'DFS', 'SYF', 'FIS', 'FI', 'PYPL', 'HOOD', 'COIN', 'KKR',
        'BX', 'APO', 'ARES', 'NDAQ', 'MSCI', 'STT', 'HIG', 'ACGL', 'RJF', 'MSTR'],
    'Healthcare': ['LLY', 'UNH', 'JNJ', 'ABBV', 'MRK', 'TMO', 'ABT', 'DHR', 'PFE', 'AMGN', 'ISRG', 'BSX',
        'MDT', 'SYK', 'GILD', 'VRTX', 'REGN', 'CI', 'ELV', 'CVS', 'HCA', 'ZTS', 'BDX', 'BMY', 'MCK', 'HUM',
        'DXCM', 'IDXX', 'BIIB', 'MRNA', 'GEHC', 'IQV', 'A', 'EW', 'CNC', 'RMD', 'COR', 'CAH', 'ALNY', 'PODD'],
    'Consumer Cyclical': ['AMZN', 'TSLA', 'HD', 'MCD', 'NKE', 'LOW', 'SBUX', 'BKNG', 'TJX', 'CMG', 'ORLY',
        'MAR', 'GM', 'F', 'ABNB', 'HLT', 'ROST', 'AZO', 'YUM', 'DHI', 'LEN', 'RCL', 'CCL', 'NCLH', 'EBAY',
        'LULU', 'DASH', 'RIVN', 'DKNG', 'EXPE', 'ULTA', 'BBY', 'DRI', 'GRMN', 'APTV', 'PHM', 'LVS', 'MGM'],
    'Consumer Defensive': ['WMT', 'COST', 'PG', 'KO', 'PEP', 'PM', 'MO', 'MDLZ', 'CL', 'TGT', 'KMB', 'GIS',
        'SYY', 'KHC', 'STZ', 'KR', 'HSY', 'KDP', 'MNST', 'ADM', 'DG', 'DLTR', 'KVUE', 'CHD', 'MKC', 'CLX',
        'K', 'HRL', 'CAG', 'TSN', 'EL', 'WBA'],
    'Communication Services': ['GOOGL', 'GOOG', 'META', 'NFLX', 'DIS', 'CMCSA', 'TMUS', 'VZ', 'T', 'CHTR',
        'WBD', 'EA', 'TTWO', 'OMC', 'RDDT', 'PINS', 'SNAP', 'SPOT', 'MTCH', 'LYV', 'NWSA', 'FOXA', 'IPG',
        'PARA', 'ROKU', 'BIDU', 'TTD'],
    'Energy': ['XOM', 'CVX', 'COP', 'SLB', 'EOG', 'MPC', 'PSX', 'VLO', 'OXY', 'WMB', 'KMI', 'OKE', 'HES',
        'DVN', 'HAL', 'BKR', 'FANG', 'TRGP', 'CTRA', 'MRO', 'APA', 'EQT', 'OVV', 'CHRD', 'AR'],
    'Industrials': ['GE', 'CAT', 'RTX', 'HON', 'UNP', 'BA', 'DE', 'LMT', 'UPS', 'ADP', 'ETN', 'GD', 'NOC',
        'EMR', 'CSX', 'NSC', 'WM', 'ITW', 'MMM', 'FDX', 'PH', 'TDG', 'GEV', 'CARR', 'OTIS', 'PCAR', 'CMI',
        'PAYX', 'ROK', 'FAST', 'ODFL', 'URI', 'CTAS', 'RSG', 'AME', 'DAL', 'UAL', 'LHX', 'DOV', 'WAB'],
    'Basic Materials': ['LIN', 'APD', 'SHW', 'FCX', 'ECL', 'NEM', 'NUE', 'DOW', 'DD', 'CTVA', 'PPG', 'VMC',
        'MLM', 'ALB', 'CF', 'MOS', 'STLD', 'IFF', 'IP', 'PKG', 'BALL', 'AMCR', 'CE', 'EMN', 'RPM', 'CLF'],
    'Utilities': ['NEE', 'DUK', 'SO', 'D', 'AEP', 'SRE', 'EXC', 'XEL', 'ED', 'PEG', 'WEC', 'ES', 'AWK',
        'PCG', 'EIX', 'DTE', 'PPL', 'FE', 'AEE', 'CEG', 'VST', 'ETR', 'CMS', 'CNP', 'NRG', 'ATO', 'LNT'],
    'Real Estate': ['PLD', 'AMT', 'EQIX', 'WELL', 'SPG', 'PSA', 'O', 'CCI', 'DLR', 'VICI', 'CBRE', 'SBAC',
        'EXR', 'AVB', 'EQR', 'IRM', 'VTR', 'ARE', 'INVH', 'WY', 'MAA', 'ESS', 'KIM', 'UDR', 'HST', 'REG'],
}
_GICS_SECTOR = {sym: sec for sec, syms in _GICS.items() for sym in syms}   # ticker → secteur GICS

# ─── GRANULARITÉ FINE : ~55 INDUSTRIES (vue « Par industrie », ≥50 secteurs distincts) ───
_INDUSTRY = {
    'Semi-conducteurs': ['NVDA', 'AMD', 'AVGO', 'QCOM', 'TXN', 'ADI', 'MU', 'MCHP', 'NXPI', 'ON', 'MPWR', 'ARM', 'TSM', 'INTC', 'GFS', 'ALAB', 'CRDO', 'SWKS', 'QRVO'],
    'Équipement semi-conducteurs': ['AMAT', 'LRCX', 'KLAC', 'TER', 'ASML', 'ENTG'],
    'Logiciel – Infrastructure': ['MSFT', 'ORCL', 'PANW', 'CRWD', 'FTNT', 'ZS', 'NET', 'DDOG', 'SNPS', 'CDNS', 'GEN', 'AKAM'],
    'Logiciel – Application': ['CRM', 'ADBE', 'NOW', 'INTU', 'WDAY', 'TEAM', 'SNOW', 'HUBS', 'APP', 'PLTR', 'ANSS', 'PTC', 'TYL', 'ADSK'],
    'Matériel & stockage': ['DELL', 'HPQ', 'HPE', 'STX', 'WDC', 'ANET', 'SMCI', 'NTAP', 'PSTG'],
    'Services IT & conseil': ['IBM', 'ACN', 'CTSH', 'INFY', 'IT', 'EPAM'],
    'Électronique & composants': ['AAPL', 'GLW', 'APH', 'TEL', 'KEYS', 'GRMN'],
    'Banques': ['JPM', 'BAC', 'WFC', 'C', 'USB', 'PNC', 'TFC', 'COF', 'MTB', 'FITB', 'RF', 'HBAN', 'KEY'],
    'Marchés de capitaux': ['GS', 'MS', 'SCHW', 'RJF', 'MSCI', 'NDAQ', 'ICE', 'CME', 'SPGI', 'MCO'],
    'Gestion d\'actifs': ['BLK', 'BX', 'KKR', 'APO', 'ARES', 'BK', 'STT', 'TROW', 'AMP'],
    'Assurance': ['CB', 'PGR', 'TRV', 'AIG', 'MET', 'PRU', 'AFL', 'ALL', 'HIG', 'ACGL', 'CINF', 'AJG', 'MMC', 'AON'],
    'Paiements': ['V', 'MA', 'AXP', 'PYPL', 'FI', 'FIS', 'GPN', 'DFS', 'SYF'],
    'Crypto & fintech': ['COIN', 'HOOD', 'MSTR', 'SOFI'],
    'Pharma': ['LLY', 'JNJ', 'ABBV', 'MRK', 'PFE', 'BMY', 'ZTS'],
    'Biotechnologie': ['AMGN', 'VRTX', 'REGN', 'GILD', 'BIIB', 'MRNA', 'ALNY', 'INCY', 'BMRN'],
    'Équipement médical': ['ISRG', 'MDT', 'SYK', 'BSX', 'BDX', 'EW', 'RMD', 'DXCM', 'IDXX', 'PODD', 'ZBH'],
    'Assurance santé': ['UNH', 'ELV', 'CI', 'CVS', 'HUM', 'CNC'],
    'Outils & diagnostics': ['TMO', 'DHR', 'ABT', 'A', 'IQV', 'MTD', 'WAT', 'RVTY'],
    'Distribution santé': ['MCK', 'COR', 'CAH', 'HCA'],
    'Commerce en ligne': ['AMZN', 'EBAY', 'MELI', 'ETSY', 'CHWY'],
    'Distribution spécialisée': ['HD', 'LOW', 'TJX', 'ROST', 'AZO', 'ORLY', 'ULTA', 'BBY', 'BURL'],
    'Restaurants': ['MCD', 'SBUX', 'CMG', 'YUM', 'DRI', 'DPZ'],
    'Voyage & loisirs': ['BKNG', 'MAR', 'HLT', 'RCL', 'CCL', 'NCLH', 'EXPE', 'ABNB', 'LVS', 'MGM', 'DKNG'],
    'Automobile': ['TSLA', 'GM', 'F', 'RIVN', 'LCID', 'APTV'],
    'Habillement & luxe': ['NKE', 'LULU', 'TPR', 'RL', 'DECK'],
    'Distribution alimentaire': ['WMT', 'COST', 'TGT', 'KR', 'DG', 'DLTR'],
    'Boissons': ['KO', 'PEP', 'MNST', 'KDP', 'STZ', 'TAP'],
    'Produits ménagers & perso': ['PG', 'CL', 'KMB', 'CLX', 'CHD', 'EL', 'KVUE'],
    'Alimentaire emballé': ['MDLZ', 'GIS', 'HSY', 'K', 'KHC', 'HRL', 'CAG', 'SYY', 'ADM', 'MKC'],
    'Tabac': ['PM', 'MO'],
    'Internet & médias sociaux': ['GOOGL', 'GOOG', 'META', 'PINS', 'SNAP', 'RDDT', 'MTCH', 'BIDU'],
    'Divertissement & streaming': ['NFLX', 'DIS', 'WBD', 'SPOT', 'ROKU', 'LYV', 'PARA', 'FOXA'],
    'Jeux vidéo': ['EA', 'TTWO'],
    'Télécoms': ['TMUS', 'VZ', 'T', 'CMCSA', 'CHTR'],
    'Pétrole & gaz E&P': ['XOM', 'CVX', 'COP', 'EOG', 'OXY', 'DVN', 'FANG', 'HES', 'APA', 'EQT', 'CTRA', 'OVV', 'MRO', 'AR', 'CHRD'],
    'Raffinage': ['MPC', 'PSX', 'VLO'],
    'Services pétroliers': ['SLB', 'HAL', 'BKR'],
    'Infrastructure énergie (midstream)': ['WMB', 'KMI', 'OKE', 'TRGP', 'LNG'],
    'Aérospatiale & défense': ['BA', 'RTX', 'LMT', 'GD', 'NOC', 'LHX', 'TDG', 'HWM'],
    'Machines & équipement': ['CAT', 'DE', 'ETN', 'EMR', 'ITW', 'PH', 'CMI', 'DOV', 'ROK', 'PCAR', 'PNR'],
    'Transport & logistique': ['UNP', 'UPS', 'FDX', 'CSX', 'NSC', 'ODFL', 'JBHT', 'URI'],
    'Compagnies aériennes': ['DAL', 'UAL', 'AAL', 'LUV'],
    'Services commerciaux': ['ADP', 'PAYX', 'CTAS', 'RSG', 'WM', 'VRSK', 'BR', 'CPRT', 'FAST'],
    'Conglomérats industriels': ['HON', 'MMM', 'GEV', 'CARR', 'OTIS', 'AME', 'ROP', 'GE'],
    'Chimie': ['LIN', 'APD', 'SHW', 'ECL', 'DD', 'DOW', 'PPG', 'CTVA', 'ALB', 'IFF', 'CE', 'EMN', 'CF', 'MOS', 'RPM'],
    'Métaux & mines': ['FCX', 'NEM', 'NUE', 'STLD', 'CLF'],
    'Matériaux de construction': ['VMC', 'MLM'],
    'Emballage': ['PKG', 'IP', 'BALL', 'AMCR'],
    'Électricité (utilities)': ['NEE', 'DUK', 'SO', 'D', 'AEP', 'EXC', 'XEL', 'ED', 'PEG', 'WEC', 'ES', 'EIX', 'DTE', 'PPL', 'FE', 'AEE', 'ETR', 'CMS', 'CNP', 'NRG', 'CEG', 'VST', 'ATO', 'LNT', 'PCG'],
    'Eau (utilities)': ['AWK', 'WTRG'],
    'REIT industriel & logistique': ['PLD', 'EXR', 'PSA'],
    'REIT télécom & data': ['AMT', 'CCI', 'EQIX', 'DLR', 'SBAC', 'IRM'],
    'REIT résidentiel': ['AVB', 'EQR', 'MAA', 'ESS', 'INVH', 'UDR'],
    'REIT commercial': ['SPG', 'O', 'REG', 'KIM', 'VICI'],
    'REIT santé': ['WELL', 'VTR', 'ARE'],
    'Immobilier services': ['CBRE'],
}
_INDUSTRY_MAP = {sym: ind for ind, syms in _INDUSTRY.items() for sym in syms}   # ticker → industrie fine
_EU_SET = list(_EUROPE)
_ASIA_SET = list(_ASIA)
# ─── COURS EN DIRECT IBKR (au bureau) : snapshot-polling du haut de l'univers ───
# Le SCORING couvre tout l'univers (967). Le LIVE est borné au top 300 (core + big +
# trend + top S&P) : ce sont les titres qui ont réellement de la data IBKR ; les small
# caps de la longue traîne n'en ont pas → elles gardent le cours du scan (différé).
# Worker = reqTickersAsync par LOTS (snapshot, lignes libérées entre lots), core en 1er.
# ⛔ LECTURE SEULE. Un titre sans abonnement data est ignoré sans crash. Cycle ~30-45s.
LIVE_SYMBOLS = UNIVERSE[:300]
TREND_SET = set(_TREND_EXTRA)   # valeurs « buzz / fast movers » → badge 🔥 dans l'UI


__all__ = [
    'WATCHLIST',
    '_BIG_EXTRA',
    '_TREND_EXTRA',
    '_SP500_EXTRA',
    '_RUSSELL_EXTRA',
    '_SECTOR_ETFS',
    '_EUROPE',
    '_ASIA',
    'UNIVERSE',
    '_DOW30',
    '_NDX100',
    '_SP500_SET',
    '_RUT_SET',
    '_GICS',
    '_GICS_SECTOR',
    '_INDUSTRY',
    '_INDUSTRY_MAP',
    '_EU_SET',
    '_ASIA_SET',
    'LIVE_SYMBOLS',
    'TREND_SET',
]

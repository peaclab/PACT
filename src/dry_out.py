
#Gffrey Vaartstra, Zihao Yuan***%
#%***Dryout biporous channel model***%
#%***20 May 2019***%
import math
import numpy as np
from sympy import Symbol
from sympy.solvers import solve

def uniform_dry_out(sigma,mu,rho,hlv,theta,t,dp,phi,AR,SF,w,L,T):
#%---Inputs---%


#%---Calculate---%
	Dh  = 2*w*AR/(1+AR)                                        #%hydraulic diameter, rect duct
	fRe = 12/((1-192/(math.pi**5*AR)*math.tanh(math.pi/(2*AR)))*(1+AR)*math.sqrt(AR)) #%Poiseuille number, rect duct
	hch = w*AR                                                #%channel height

    #Pb   = 1 - dp/(4*sigma*math.cos(math.radians(theta))) * qin/(rho*hlv*(1-SF)) * mu * (fRe/(Dh**2)*(L**2)/hch+ 32/(dp**2)*t/phi)        #%dimensionless pressure budget
	qdry = (4*sigma*math.cos(math.radians(theta))/dp*(mu/(rho*hlv*(1-SF)) * (32/(dp**2)*t/phi + fRe/(Dh**2)*(L**2)/(w*AR)))**-1) * 1e-4    #%dryout heat flux, w/cm2
   
	return qdry



def hotspot_dry_out(t,dp,phi,AR,SF,w,coolant):
	if coolant == 0:
		#water property
		sigma   = 0.0679    #%surface tension, [N/m]
		mu      = 5.4650e-04    #%liquid dynamic viscosity, [Pa*s]
		rho     = 987.9962    #%liquid density, [kg/m3]
		hlv     =  2.3819e+06    #%latent heat of vape, [J/kg]
	elif coolant == 1:
		#R245fa
		sigma   = 0.0105    #%surface tension, [N/m]
		mu      = 2.8917e-04    #%liquid dynamic viscosity, [Pa*s]
		rho     = 1267.4    #%liquid density, [kg/m3]
		hlv     = 1.7464e+05   #%latent heat of vape, [J/kg]
	else:
		#R141B
		sigma   = 0.0152    #%surface tension, [N/m]
		mu      = 3.1102e-04    #%liquid dynamic viscosity, [Pa*s]
		rho     = 1184.0    #%liquid density, [kg/m3]
		hlv     = 2.1378e+05   #%latent heat of vape, [J/kg]

	theta = 10
	t = t*1e-6
	dp = dp*1e-6
	w = w*1e-6

	T   = 50+273.15;        #%temperature, [K]
	qbg = 50e4;             #%background heat flux [W/m2]
	q2 = Symbol('q2')                #%hotspot heat flux [W/m2]

	#%---Chip Inputs---%
	Lx = 20e-3; Ly = 20e-3;   #%chip dimensions [m]
	n = 2; m = 2;       #%number of rows, columns of hotspots
	xhs = 0.5e-3; yhs = 0.5e-3; #%hs dimensions [m]
	dx = 7e-3; dy = 7e-3;   #%hs spacing

	#%---Properties---%
	#sigma  = 0.0679    #%surface tension, [N/m]
	#mu  = 5.4650e-04    #%liquid dynamic viscosity, [Pa*s]
	#rho = 987.9962    #%liquid density, [kg/m3]
	#hlv  =  2.3819e+06    #%latent heat of vape, [J/kg]

	#%---"Discretize" space---%
	xsym    = Lx/2
	mq      = m/2
	if mq%1 == 0:
		edges = 2*mq+1
		edges = int(edges)
		x = np.zeros(edges)
		x[0] = xsym - mq*xhs - dx*(mq-0.5)
		x[-1] = xsym
		if mq>1:
			for i in range(1,edges-1,2):
				x[i] = x[i-1] + xhs
				x[i+1]= x[i] + dx
		else:
			x[1] = x[0] + xhs
	else:
		if xsym - mq*xhs - dx*math.floor(mq) == 0:   #%in case hs touches edge
			edges = 2*math.ceil(mq)-1;
			edges = int(edges)
			x = np.zeros(edges);
			x[0] = 0;
			x[-1] = xsym;
			if mq>1:
				for i in range(1,edges-2,2):
					x[i] = x[i-1] + xhs;
					x[i+1] = x[i] + dx;


		else:
			edges = 2*math.ceil(mq)
			edges = int(edges)
			x = np.zeros(edges)
			x[0] = xsym - mq*xhs - dx*math.floor(mq)
			x[-1] = xsym
			if mq>1:
				for i in range(1,edge-2,2):
					x[i] = x[i-1] + xhs;
				x[i+1] = x[i] + dx; 

	qind = np.zeros(edges)
	if len(x) == 1:
		qind = 1
	    


	elif x[0]>0:    
		for i in range(0,edges):
			if (i+1)%2==0:
				qind[i] = 1   #%indicates hs heat flux
			else:
				qind[i] = 0   #%indicates bg heat flux
		
	    
	else:
		for i in range(0,edges):
			if (i+1)%2==0:
				qind[i] = 0 
			else:
				qind[i] = 1 
	x = np.insert(x, 0, 0, axis=0)

	#%---Calculate dryout---%
	Pmax = 4*sigma*math.cos(math.radians(theta))/dp
	Dh  = 2*w*AR/(1+AR)                                    # %hydraulic diameter, rect duct
	fRe = 12/((1-192/(math.pi**5)*AR*math.tanh(math.pi/(2*AR)))*(1+AR)*math.sqrt(AR)) #%Poiseuille number, rect duct
	hch = w*AR

	#%--Determine velocity at inlet--%
	v0 = 0;
	for i in range(1,edges+1):
		if qind[i-1] == 1:
			q = q2
		else:
			q = qbg
		v0 = v0 + q*(x[i]-x[i-1]);  #%lacks prefactor, goes outside of integral
	#%--Build sum of pressure drops--%
	fun = 0;
	for i in range(1,edges+1):
		if qind[i-1] == 1:
			q = q2
		else:
			q = qbg
	    
		sum_dum = 0;
		k = 1;
		while k<i:
			if qind[i-1] == 1:
				qk = q2
			else:
				qk = qbg
	       
			sum_dum = sum_dum + qk*(x[k]-x[k-1]);
			k = k+1;
	    
		fun = fun + v0*(x[i]-x[i-1]) - sum_dum*(x[i]-x[i-1]) + q*x[i-1]*(x[i]-x[i-1]) - q/2*(x[i]**2-x[i-1]**2);

	fun = 2*fRe*mu/((Dh**2)*rho*hlv*(1-SF)*hch)*fun + 32/(dp**2)*mu*t*q/(rho*hlv*phi*(1-SF));

	qhs = solve(Pmax-fun,q2)  #%dryout heat flux [W/cm2]  
	qhs = qhs[0]* 1e-4
	return qhs

print(hotspot_dry_out(0.7,0.15,0.45,2,0.1,8,0))		

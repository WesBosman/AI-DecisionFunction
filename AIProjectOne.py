import itertools
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as matplot
from matplotlib.lines import Line2D

# Male: 0 Female: 1
# Average Man for my Sample:   5'9" , 185 lbs
# Average Woman for my Sample: 5'4" , 145 lbs
meanWeightMale, stdDevWeightMale = 185.0, 10.0
meanHeightMale, stdDevHeightMale =	5.9, 0.2
meanWeightFemale, stdDevWeightFemale = 145, 10
meanHeightFemale, stdDevHeightFemale = 5.4, 0.2
# Data points for the line that seperates the two plots in figure 2
x1, y1 = 4.53, 225.0
x2, y2 = 6.8, 100

male_c = 0.0
male_e = 0.0
female_c = 0.0
female_e = 0.0

def main():
	# Random distributions for height and weight for Male and Female
	np.random.seed(2048)
	heightMale = np.random.normal(meanHeightMale, stdDevHeightMale, 2000)
	weightMale = np.random.normal(meanWeightMale, stdDevWeightMale, 2000)
	heightFemale = np.random.normal(meanHeightFemale, stdDevHeightFemale, 2000)
	weightFemale = np.random.normal(meanWeightFemale, stdDevWeightFemale, 2000)
	# Setup Arrays for Males and Females as well as a combined array for printing to file
	maleArray = [Male]
	femaleArray = [Female]
	combinedArray = []
	i = 1
	# Create and array of Male Objects
	for(h, w) in itertools.izip(heightMale, weightMale):
		man = Male(h, w, 0.0)
		combinedArray.append(man)
		i+= 1
		
	# Create an array of Female Objects
	for (h, w) in itertools.izip(heightFemale, weightFemale):
		woman = Female(h, w, 1.0)
		combinedArray.append(woman)
		i+= 1
	
	# Generate the results for Males and Females
	print_results(combinedArray)

	# Set up the graphs then plot them
	plot_height(combinedArray)
	
	#plot_height(heightMale, heightFemale)
	plot_height_and_weight(heightMale, weightMale, heightFemale, weightFemale)
	plt.show()

	
# Calculate wether the point is above or below the line
def above_or_below(x1, y1, mX, y0, figure, gender):
	global male_c
	global male_e
	global female_c
	global female_e
	
	male_correct = 0.0
	male_error = 0.0
	female_correct = 0.0
	female_error = 0.0
	
	for(x,y) in itertools.izip(x1,y1):
		my_y = x * mX + y0
		
		# Male
		if(gender == 0):
			if y >= my_y:
				male_c = male_c + 1
				
			else:
				male_e = male_e + 1
				
		# Female	
		elif(gender == 1):
			if y >= my_y:
				female_e = female_e + 1
				
			else:
				female_c = female_c + 1

	if ((male_e and male_c) and (female_e and  female_c)):
		print("Calculating Accuracy")
		ftotal = float(female_e + female_c)
		mtotal = float(male_e + male_c)
		#green_plus = "\033[1;32;40m[+]\033[0m"
		#red_minus = "\033[1;31;40m[-]\033[0m"
		print("")
		print("[+] Female Correct %.2f" % (female_c))
		print("[+] Female Error:  %.2f  "  % (female_e))
		print("[+] Female Total:  %.2f  "  % (ftotal))
		print("[+] Female Error As Percent:    %.2f%% " % ((female_e / ftotal) * 100))
		print("[+] Female Correct As Percent: %.2f%% " % ((female_c / ftotal) * 100))
		print("")
		print("[+] Male Correct: %.2f " % (male_c))
		print("[+] Male Error:   %.2f  "   % (male_e))
		print("[+] Male Total:   %.2f  "   % (mtotal))
		print("[+] Male Error As Percent:    %.2f%% " % ((male_e / mtotal) * 100))
		print("[+] Male Correct As Percent: %.2f%% " % ((male_c / mtotal) * 100))
		print("")
		create_confusion_matrix(female_c, female_e, male_c, male_e)
		

def create_confusion_matrix(fc, fw, mc, mw):
	print("Creating Confusion Matrix")
	print("[+] Classes      Male      Female      Total")
	print("[+] Male         %.2f     %.2f       %.2f" %(mc, mw, (mc + mw)))
	print("[+] Female       %.2f     %.2f       %.2f" %(fw, fc, (fc + fw)))



# Calculate the midpoint between two points
def midpoint(x1, x2, y1, y2):
	deltaX = x1+x2
	deltaY = y1+y2
	return (float(deltaX/2), float(deltaY/2))
	

# Detect the type of figure matplotlib is using to display the graphs.
# From: cxrodgers on stackoverflow.
# I am unsure if this program will be portable to Windows or Mac?
def figure_type(f, x, y):
    backend = plt.get_backend()
    if backend == 'TkAgg':
        f.canvas.manager.window.wm_geometry("+%d+%d" % (x, y))
    elif backend == 'WXAgg':
        f.canvas.manager.window.SetPosition((x, y))
    else:
        # This works for QT and GTK
        # You can also use window.setGeometry
    	f.canvas.manager.window.move(x, y)
    	

# Plot the height one dimensonaly 
def plot_height(combinedArray):
	# Split up the objects from the combined array based on height
	woman = []
	man = []
	for (person) in (combinedArray):
		#print("%s: %.2f" %(person.gender, person.height))
		# Person is a male
		if person.gender == 0:
			man.append(person.height)
			
		else:
			woman.append(person.height)
		
	# Plot the data using scatter plots
	figure = plt.figure(1)
	#figure_type(figure, 0, 500)
	figure.suptitle("AI Project One (Part A)", fontsize=16, fontweight='bold')
	midx, midy = midpoint(meanHeightFemale, meanHeightMale, 0, 0)
	ax2 = figure.add_subplot(111)
	plt.plot([midx,midx], [-1, 1], color='orange', linestyle='-', linewidth=2)
	
	plt.title("Wes Bosman")
	plt.axis([4, 7, -1, 1])
	plt.xlabel("Height")
	#plt.ylabel("Height")
	plt.annotate("y = 5.65", xy=(5.05, 0.25))
	x = [0, 0.01]
	y = [(man), (woman)]
	
	for xe, ye in zip(x,y):
		# Men get squares Females get triangles
		if xe:
			print("Creating Graph for Women based on Height")
			#plt.scatter([xe] * len(ye), ye, marker='^', color="red", label="Female")
			plt.scatter(ye, [xe] * len(ye), marker='^', color="red", label="Female")
		else:
			print("Creating Graph for Men based on Height")
			plt.scatter(ye, [xe] * len(ye), marker='s', color="blue", label="Male")
			#plt.plot(xe, ye, marker='s', color="blue", label="Male")
	
	#plt.xticks([5.0, 6.0])
	#plt.axes().set_xticklabels(["Female", "Male"])
	plt.legend(loc="upper right")
	
	# Write to seperator file for problem a
	sep_line_a(midx, midy)
	
	# Save figure_1 Graph
	print("Saving Figure 1 Graph")
	plt.savefig("figure_1.png")
	
	
	
def plot_height_and_weight(heightMale, weightMale, heightFemale, weightFemale):
	print("Creating Graph for Men and Women based on Weight and Height")
	
	# Figure out the slope and y intercept of the points entered
	line = Line(x1, x2, y1, y2)
	print("Line Bisecting Men and Women based on Height and Weight: %s"  %line)
	
	# Plot the data for male and female height and weight
	figure = plt.figure(2)
	#figure_type(figure, 500, 500)
	figure.suptitle("AI Project One (Part B)", fontsize=16, fontweight='bold')
	ax = plt.axes()
	ax1 = figure.add_subplot(111)
	plt.title("Wes Bosman")
	plt.xlabel("Height")
	plt.ylabel("Weight")
	plt.axis([4, 7, 100, 225])
	plt.plot(heightMale, weightMale, 'bs', label="Male")
	plt.plot(heightFemale, weightFemale, 'r^', label="Female")
	plt.plot([x1, x2], [y1, y2], color='orange', linestyle='-', linewidth=2)
	plt.annotate(line, xy=(4.05, 195))
	plt.legend(loc="upper right")
	
	slope = line.get_slope()
	y_intercept = line.get_y_intercept()
	
	# Write to seperator file for problem b
	sep_line_b(slope, y_intercept)
	
	# Print what the standard deviations and means were
	print("")
	print("[+] Mean Weight for Males: %.2f , Standard Deviation: %.2f lbs" %(meanWeightMale, stdDevWeightMale))
	print("[+] Mean Height for Males: %.2f   , Standard Deviation: %.2f in" %(meanHeightMale, stdDevHeightMale))
	print("[+] Mean Weight for Females: %.2f , Standard Deviation: %.2f lbs" %(meanWeightFemale, stdDevWeightFemale))
	print("[+] Mean Height for Females: %.2f   , Standard Deviation: %.2f in" %(meanHeightFemale, stdDevHeightFemale))
	print("")
	
	# Are the data points above or below the line for males? 
	above_or_below(heightMale, weightMale, slope, y_intercept, "figure_2", 0)
	
	# Are the data points above of below the line for females?
	above_or_below(heightFemale, weightFemale, slope, y_intercept, "figure_2", 1)

	# Save figure
	print("Saving Figure 2 Graph")
	plt.savefig("figure_2.png")
	
	
# Consider only height
def sep_line_a(a, b):
	print("Writing to sep_line_a.txt")
	with open("sep_line_a.txt", "w") as file:
		file.write("%.2f\n%d" %(a,1))

# Consider height and weight
def sep_line_b(a, b):
	print("Writing to sep_line_b.txt")
	with open("sep_line_b.txt", "w") as file:
		file.write("%.2f\n%.2f\n%d" %(a,b,1))
	
# Print the results to a file
def print_results(a):
	print("Writing to data.txt")
	with open("data.txt", "w") as file:
		for person in a:
			file.write("%.2f, %.2f, %d\n" %(person.height, person.weight, person.gender))

# Class for calculating the line that seperates the two plots
class Line():
	slope = 0.0
	b=0.0
	
	def __init__(self, x1, x2, y1, y2):
		self.slope = (y2-y1)/(x2-x1)
		self.b = y1-self.slope*x1
	
	def get_slope(self):
		return self.slope
	
	def get_y_intercept(self):
		return self.b
		
	def __str__(self):
		return "y = %.2fx + %.2f" %(self.slope, self.b)

# Class for Male Objects
class Male():
	height = 0.0
	weight = 0.0
	gender = 0
	
	def __init__(self, height, weight, gender):
		self.height = height
		self.weight = weight
		self.gender = gender
	
	def __str__(self):
		h = self.height
		w = self.weight
		g = self.gender
		ret_str = "Height: %.2f, Weight: %.2f, Gender: Male %.2f" %(h, w, g)
		return ret_str

# Class for Female Objects
class Female():
	height = 0.0
	weight = 0.0
	gender = 1
	
	def __init__(self, height, weight, gender):
		self.height = height
		self.weight = weight
		self.gender = gender
	
	def __str__(self):
		h = self.height
		w = self.weight
		g = self.gender
		ret_str = "Height: %.2f, Weight: %.2f, Gender: Female %.2f" %(h, w, g)
		return ret_str

if __name__ == "__main__":
	main()

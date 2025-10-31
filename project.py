import numpy as np
import matplotlib.pyplot as plt


def longest_palindrome(bits):
    longest=""
    for i in range (len(bits)):
        for j in range (len(bits)+1):
            part=bits[i:j]
            if part==part[::-1]:#(-1 means reverse direction so start from end go till start and step=-1, this reverses the string )
                if len(part)>len(longest):
                    longest=part
    return longest


# Function to plot signal: time along x-axis and amplitude along y-axis.
def plot_signal(time, signal, title="LINE ENCODING SCHEME"):
    plt.figure(figsize=(10, 4))
    plt.axhline(0, color="#444", linewidth=1.2)

    # Elegant step line with smooth color
    plt.step(time, signal, where="post", linewidth=2.8, color="#0077b6")
    plt.fill_between(time, signal, 0, step="post", alpha=0.25, color="#90e0ef")

    plt.title(title, fontsize=15, fontweight="bold", color="#222222", pad=15)
    plt.xlabel("Time", fontsize=12)
    plt.ylabel("Amplitude", fontsize=12)

    plt.grid(True, linestyle="--", alpha=0.5)
    plt.gca().set_facecolor("#fdfdfd")

    # Rounded axes style
    for spine in plt.gca().spines.values():
        spine.set_visible(False)

    plt.ylim(-1.6, 1.6)
    plt.xlim(time[0], time[-1])
    plt.minorticks_on()
    plt.tick_params(axis='both', which='major', labelsize=10)
    plt.tight_layout()
    plt.show()



# Digital to Digital encoding schemes:
# 1. NRZ-L
def NRZ_L(bits):
    signal=[]
    time=[]
    prev=0
    for bit in bits:    # Unique levels assigned to 0 and 1 bit.
        if bit=="1":
            level=1
        else:
            level=-1
        time.extend([prev,prev+1])
        signal.extend([level,level])

        prev=prev+1

    return time,signal

# 2. NRZ-I
def NRZ_I(bits):
    signal=[]       
    time=[]        
    prev=0            
    last_level = -1    # Ensuring that Positive logic will be followed for the first time (-1 * -1 = 1).

    for bit in bits:
        if bit=='1' or bit==1:    
            last_level=last_level*(-1)    # Inverting Amplitude if bit = 1. 
        time.extend([prev,prev+1])
        signal.extend([last_level,last_level])

        prev=prev+1

    return time,signal

# 3. Manchester
def Manchester(bits):
    signal=[]
    time=[]
    prev=0
    for bit in bits:
        if bit=="1":    # Unique levels assigned to 0 and 1 bit, but transition in the middle.
            first_half=1
            second_half=-1
        else:
            first_half=-1
            second_half=1
        signal.extend([first_half,second_half,second_half])   # Signal levels for start, mid-bit transition till the next bit.
        time.extend([prev,prev+0.5,prev+1])   # Time at the start, middle and end of the bit.
        prev=prev+1
    return time, signal

# 4. Differential_Manchester
def Differential_Manchester(bits):
   signal=[]
   time=[]
   last_level=1
   prev=0
   for bit in bits:
       
        if bit=="0":
            last_level=last_level*-1   # Inverting Amplitude if bit = 0, else starting where the last signal ended.

        first_half=last_level
        second_half=-last_level  

        signal.extend([first_half,second_half,second_half])   # Signal levels for start, mid-bit transition till the next bit.
        time.extend([prev,prev+0.5,prev+1])   # Time at the start, middle and end of the bit.
        
        prev=prev+1
        last_level =second_half    # Ensuring the new bit starts at the amplitude where the last one ended.
   return time,signal 

# 5. AMI
def AMI(bits):
    signal=[]
    time=[]
    last_polarity=-1   # Ensuring that Positive logic will be followed for the first time (-1 * -1 = 1).
    prev=0
    for bit in bits:
        if bit=="1" or bit=="B":   # Follows AMI rule in case of B or 1, i.e. alternating amplitude 
            last_polarity=last_polarity*(-1)
            level=last_polarity

        elif(bit=="V"):   # Violating AMI rule in case of V.
            level=last_polarity
            
        else:   # Amplitude 0 if bit = 0.
            level=0
        signal.extend([level,level])
        time.extend([prev,prev+1])
        prev=prev+1
    return time,signal

# Scrambing methods for AMI in case of long string of 0s.
def HDB3(bits):
    bits=list(bits) 
    no_of_Ones=0
    i=0
    while i<len(bits):
        if bits[i:i+4]==['0','0','0','0']:
            if no_of_Ones % 2==0:
                bits[i]="B"
                bits[i+1]="0"
                bits[i+2]="0"
                bits[i+3]="V"
            else:
                bits[i]="0"
                bits[i+1]="0"
                bits[i+2]="0"
                bits[i+3]="V"
            no_of_Ones=0
            i=i+4
        else:
            if bits[i]=="1":
                no_of_Ones=no_of_Ones+1
            i=i+1
    return bits

def B8ZS(bits):
    bits=list(bits)
    i=0
    while i<len(bits):
        if bits[i:i+8]==["0","0","0","0","0","0","0","0"]:
            bits[i:i+8]=["0","0","0","V","B","0","V","B"]
            i=i+8
        else:
            i=i+1
    return bits

# Analog to Digital encoding schemes:
# 1. PCM
def PCM():

    # User will provide sampled amplitudes.
    samples=list(map(float, input("Enter sampled analog values (comma-separated): ").split(',')))

    levels=list(range(-3,5))  # For Quantization, 8 levels are created.

    if any(x<-3 or x>4 for x in samples):
        print("\n Error: Range not defined! Please enter values between -3 and +4 only.")
        return  

    level_to_code = {level: i for i, level in enumerate(levels)}

    print("\nQuantization Levels and Codes:")
    for level, code in level_to_code.items():   # Assigning Quantization levels to amplitude, and generating the 3 bit binary code for that level.
        print(f"{level:>2} → {code:03b}")

    quantized=[min(levels,key=lambda L: abs(L - x)) for x in samples]
    print("\nQuantized Values:",quantized)

    binary_codes=[format(level_to_code[q],'03b') for q in quantized]
    print("Binary Codes:", binary_codes)

    bitstream = ''.join(binary_codes)
    print("\nFinal Bitstream:", bitstream)
    pal=longest_palindrome(bitstream)
    print(f"\nLongest Palindrome in Bitstream: {pal}")

    
    # The bitstream obtained is fed into any one of the digital line encoding schemes.
    print("\nAvailable Digital Encodings:")
    print("1: NRZ-L")
    print("2: NRZ-I")
    print("3: Manchester")
    print("4: Differential Manchester")
    print("5: AMI")

    choice = input("Enter your choice (1-5): ").strip()
    if choice=="1":
        t,s=NRZ_L(bitstream)
        plot_signal(t,s,"NRZ-L encoding")
    elif choice=="2":
        t,s=NRZ_I(bitstream)
        plot_signal(t,s,"NRZ-I encoding")
    elif choice=="3":
        t,s=Manchester(bitstream)
        plot_signal(t,s,"Manchester encoding")
    elif choice=="4":
        t,s=Differential_Manchester(bitstream)
        plot_signal(t,s,"Differential_Manchester encoding")
    elif choice=="5":
        t,s=AMI(bitstream)
        scramble=input("Apply Scrambling?? (yes/no) ").strip().lower()
        if scramble=="yes":
            scrambling_type=input("Choose type : (B8ZS/HDB3): ").strip().upper()
            if scrambling_type == "B8ZS":
                scrambled_data = B8ZS(bitstream)
            elif scrambling_type == "HDB3":
                scrambled_data = HDB3(bitstream)
            else:
                print("INVALID SCRAMBLING TECHNIQUE")
                return

            t, s = AMI(scrambled_data)
            plot_signal(t, s, f"AMI with {scrambling_type} Scrambling")

               
        else:
            plot_signal(t,s,"ami encoding")
    else:
            print("Invalid choice.")

# 2. DM
def Delta_Modulation():
    
    # User will provide sampled amplitudes.
    samples =list(map(float,input("Enter sampled (quantized) values (comma-separated): ").split(',')))

    if len(samples)<2:
        print(" ERROR! At least two samples required for Delta Modulation")
        return

    bitstream=[]

    for i in range(1,len(samples)):    # If the amplitude is greater than previous amplitude, bit = 1. else 0.
        if samples[i]>samples[i-1]:
            bitstream.append('1')  
        else:
            bitstream.append('0')  

    bitstream_str = ''.join(bitstream)

    print("\nInput Samples: ",samples)
    print("Delta Modulation Bitstream: ",bitstream_str)
    pal=longest_palindrome(bitstream_str)
    print(f"\nLongest Palindrome in Bitstream: {pal}")



    # The bitstream obtained is fed into any one of the digital line encoding schemes.
    print("\nAvailable Digital Encodings:")
    print("1: NRZ-L")
    print("2: NRZ-I")
    print("3: Manchester")
    print("4: Differential Manchester")
    print("5: AMI")

    choice = input("Enter your choice (1-5): ").strip()
    if choice=="1":
        t,s=NRZ_L(bitstream_str)
        plot_signal(t,s,"NRZ-L encoding")
    elif choice=="2":
        t,s=NRZ_I(bitstream_str)
        plot_signal(t,s,"NRZ-I encoding")
    elif choice=="3":
        t,s=Manchester(bitstream_str)
        plot_signal(t,s,"Manchester encoding")
    elif choice=="4":
        t,s=Differential_Manchester(bitstream_str)
        plot_signal(t,s,"Differential_Manchester encoding")
    elif choice=="5":
        t,s=AMI(bitstream_str)
        scramble=input("Apply Scrambling?? (yes/no) ").strip().lower()
        if scramble=="yes":
            scrambling_type=input("Choose type : (B8ZS/HDB3): ").strip().upper()
            if scrambling_type == "B8ZS":
                scrambled_data = B8ZS(bitstream_str)
            elif scrambling_type == "HDB3":
                scrambled_data = HDB3(bitstream_str)
            else:
                print("INVALID SCRAMBLING TECHNIQUE")
                return

            t, s = AMI(scrambled_data)
            plot_signal(t, s, f"AMI with {scrambling_type} Scrambling")

               
        else:
            plot_signal(t,s,"ami encoding")
    else:
            print("Invalid choice.")
    

### The main function to drive the encoder. ###
def main():
    print(" LINE ENCODING VISUALIZER ")

    signal_type = input("Enter type (DIGITAL / ANALOG): ").strip().lower()

    if signal_type == "digital":
        data = input("Enter Binary Data (e.g. 10101110): ").strip()
        pal=longest_palindrome(data)
        print(f"\nLongest Palindrome in Bitstream: {pal}")
        print("\nAvailable Digital Encodings:")
        print("1: NRZ-L")
        print("2: NRZ-I")
        print("3: Manchester")
        print("4: Differential Manchester")
        print("5: AMI")

        choice = input("Enter your choice (1-5): ").strip()
        if choice=="1":
            t,s=NRZ_L(data)
            plot_signal(t,s,"NRZ-L encoding")
        elif choice=="2":
            t,s=NRZ_I(data)
            plot_signal(t,s,"NRZ-I encoding")
        elif choice=="3":
            t,s=Manchester(data)
            plot_signal(t,s,"Manchester encoding")
        elif choice=="4":
            t,s=Differential_Manchester(data)
            plot_signal(t,s,"Differential_Manchester encoding")
        elif choice=="5":
            t,s=AMI(data)
            scramble=input("Apply Scrambling?? (yes/no) ").strip().lower()
            if scramble=="yes":
                scrambling_type=input("Choose type : (B8ZS/HDB3): ").strip().upper()
                if scrambling_type == "B8ZS":
                    scrambled_data = B8ZS(data)
                elif scrambling_type == "HDB3":
                    scrambled_data = HDB3(data)
                else:
                    print("INVALID SCRAMBLING TECHNIQUE")
                    return

                t, s = AMI(scrambled_data)
                plot_signal(t, s, f"AMI with {scrambling_type} Scrambling")

               
            else:
                plot_signal(t,s,"ami encoding")
        else:
            print("Invalid choice.")

    elif signal_type == "analog":
        print("Available Analog Encodings:")
        print("1. PCM")
        print("2. Delta Modulation")
        choice = input("Enter choice (1 or 2): ").strip()

        if choice == "1":
            PCM() 
        elif choice == "2":
            Delta_Modulation()
        else:
            print("Invalid choice.")

    
    else:
        print("Invalid input type. Please enter DIGITAL or ANALOG.")


    
if __name__ == "__main__":
    main()
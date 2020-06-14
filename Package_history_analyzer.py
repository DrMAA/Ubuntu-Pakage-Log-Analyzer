import gzip,os,glob
#final_content is the header of the resulting *.csv file
final_content="Pkg,State,PkgMgr,Date,From file\n"

#function to process history.gz files
def process(fname):
    with gzip.open(fname, 'rb') as f:
        #divide file into blocks with different date-time stamps
        content = f.read().strip().split("\nStart-Date: ")[1:]
    
    #refer to the csv header created outside the function
    global final_content
    
    for block in content:
        #process lines of each block
        block_rows=block.split("\n")[1:]
        
        if block_rows[0].find("apt-get install")>=0:
            #get rid of the "--no-install-recommends" flag, and extract package names
            pkg_list=block_rows[0].replace("--no-install-recommends","").split(" apt-get install ")[1].split(" ")
            for pkg in pkg_list:
                if pkg!="":
                    final_content+="%s,Install,apt-get,%s,%s\n"%(pkg,block.split("\n")[0],fname)
        elif block_rows[0].find("apt install")>=0:
            #todo
            pass
        elif block_rows[0].find("apt-get purge")>=0:
            pkg_list=block_rows[0].split("apt-get purge ")[1].split(" ")
            for pkg in pkg_list:
                final_content+="%s,Purge,apt-get,%s,%s\n"%(pkg,block.split("\n")[0],fname)
        elif block_rows[0].find("dpkg -i")>=0:
            #todo
            pass
        elif block_rows[0].find("dpkg -r")>=0:
            #todo
            pass
        elif block_rows[0].find("/usr/sbin/synaptic")>=0:
            if block_rows[1].startswith("Install: ") or block_rows[1].startswith("Reinstall: "):
                pkg_list=block_rows[1].split("all: ")[1].split("), ")
                for pkg in pkg_list:
                    final_content+="%s,Install,Synaptic,%s,%s\n"%(pkg.split(":")[0],block.split("\n")[0],fname)
            elif block_rows[1].startswith("Purge: "):
                pkg_list=block_rows[1].split("rge: ")[1].split("), ")
                for pkg in pkg_list:
                    final_content+="%s,Purge,Synaptic,%s,%s\n"%(pkg.split(":")[0],block.split("\n")[0],fname)
    
os.chdir("/var/log/apt")
lst=glob.glob("history*.gz")
for i in lst:
    print "processing file: ",i
    process("/var/log/apt/"+i)

f=open("/home/"+os.listdir("/home/")[0]+"/Desktop/AppPkgStatusReport.csv","w")
f.write(final_content.strip())
f.close()
print "\nProcessed a total of %d files, output was written to: "%lst.__len__(),"/home/"+os.listdir("/home/")[0]+"/Desktop/AppPkgStatusReport.csv"

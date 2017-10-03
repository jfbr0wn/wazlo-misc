# THIS CODE WILL DOWNLOAD 1000 RESUMES

from bs4 import BeautifulSoup
import urllib3
import certifi
import time
import os

# find all function to look for strings in text
def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub)

# setting up the pool manager
http = urllib3.PoolManager(cert_reqs = 'CERT_REQUIRED', ca_certs=certifi.where())

# list of cities, be careful when uncommenting more than one as it will start from "pagestart" on each of those cities
search_where = [
    ##'Atlanta',
    ##'Austin',#
    ##'Boston',#
    ##'Boulder',#
    ##'Chicago',
    ##'Dallas',
    ##'Denver',
    ##'Houston',
    ##'Las Vegas',
    ##'Los Angeles',
    ##'Miami',
    ##'Minneapolis',
    ##'Minnetonka',
    ##'New Jersey',
    ##'New York',
    ##'Oakland',
    ##'Phoenix',
    ##'Pittsburgh',
    ##'Portland',
    ##'Raleigh',
    ##'Redwood City',
    ##'Rochester',
    ##'Sacramento',
    ##'Salt Lake City',
    ##'San Francisco',
    ##'San Francisco Bay Area',
    ##'San Jose',
    ##'Seattle',
    ##'St.Louis',
    ]

def main():
    # for each city
    for count in range(0, len(search_where)):
        # replace the spaces with "+".  This is so it can be copied straight into the website link to search
        search_where[count] = search_where[count].replace(' ', '+')
        
        # which page the algorithm starts (0 means first page, limit is 19 as there are max 20 pages.  error will show in text if its over 19)
        pagestart = 0
        # this is for the website url link
        pagestart *= 50
        # runs through all pages from pagestart onwards (page 1 to 20 or pagestart 0 to 19)
        while (True):
            #prints the page its starting on
            print('page ' + str(int((pagestart/50) +1)) + ' start')
            
            # sets the url to pull from and grabs all the text from the HTML text
            url = 'https://www.indeed.com/resumes?q=&l=' + search_where[count] + '&co=US&start=' + str(pagestart)
            response = http.request('GET', url)
            soup = BeautifulSoup(response.data, 'lxml')
            text = str(soup)
            
            # checks to see if its the 21+ page and breaks out of the loop
            if list(find_all(text, 'The page you are looking for was not found')) != []:
                break
            
            # finds the round about location of all the ids and lists them, should be 50 of them
            ids = list(find_all(text, 'data-rez'))
            
            # for all 50 ids
            for result in range(0, len(ids)):
                # obtains the id by grabbing the ID from the relative position based upon the unique search term above
                resume_id = text[ids[result]+10:ids[result]+26]
                # prints the ID
                print(resume_id)
                
                # added to try and fix the locking out from overpulling
                #time.sleep(1)
                
                # grabs the pdf download_url
                download_url = 'https://www.indeed.com/r/' + resume_id + '/pdf'
                response2 = http.request('GET', download_url)
                
                # changes directory to be the correct one
                if not os.path.exists('resumes/' + search_where[count]):
                    os.makedirs('resumes/' + search_where[count])
                
                # writes it as a file in that directory
                with open('resumes/' + search_where[count] + '/' + resume_id+'.pdf', 'wb') as f:
                    f.write(response2.data)
                    f.close()
                
            # prints that its ending the lage
            print('page ' + str(int((pagestart/50) +1)) + ' end')
            # incrementing to next page
            pagestart += 50
            #if pagestart / 50 in [5, 10, 15, 20]:
            #    time.sleep(7200)
        
        # prints out the end of the loop    
        print('no page ' + str(int((pagestart/50) +1)))
        print('Finished ' + search_where[count])

    # prints the full end of downloads
    print('Finished all downloads')

if __name__ == "__main__":
    main()

# END OF CODE
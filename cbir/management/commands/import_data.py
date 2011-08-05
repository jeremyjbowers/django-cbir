from django.core.management.base import BaseCommand, CommandError
from BeautifulSoup import BeautifulSoup
import urllib2
from cbir.models import Year, Lawmaker, Earmark
from django.template.defaultfilters import striptags, slugify
from sets import Set

class Command(BaseCommand):

    def handle(self, *args, **options):
        '''
        Defines a function that imports data from cbir urls.
        '''
        # Get all of the Year objects.
        # Right now, we'll cut this to one.
        years = Year.objects.all().order_by('-year')
        
        # Loop through each of the years above.
        for year in years:
            
            # For this year, get the earmark_url and open it with urllib2.
            response = urllib2.urlopen(year.get_earmark_url())
            
            # Read the response so that we can have some HTML.
            html = response.read()
            
            # Pass the HTML to beautiful soup for parsing.
            soup = BeautifulSoup(html)
            
            # From the soup, get the table.
            table = soup.find('table')
            
            # From the table, get all of the rows.
            rows = table.findAll('tr')
            
            # Loop through the rows.
            for row in rows:
                
                # For this row, find the cells.
                cells = row.findAll('td')
                
                try:
                    line_number = int(cells[0].contents[0])
                except:
                    pass
                
                try:
                    tracking_number = int(cells[1].contents[0])
                except:
                    pass
                
                try:
                    title = striptags(cells[3].contents[0])
                    title = title.replace('\r', '').replace('\n', '').replace('\r\n', '').replace('&rsquo;', "'").replace("  ", " ")
                except:
                    pass
                
                try:
                    detail_url = cells[3].contents[0]['href']
                    detail_url = u'%s%s' % (year.get_base_url(), detail_url)
                except:
                    pass
                    
                try:
                    amount = int(cells[4].contents[0].replace(',', ''))
                except:
                    pass
                
                try:
                    if cells[2].contents != 'Originating':
                        lawmaker, created = Lawmaker.objects.get_or_create(dirty_name=slugify(cells[2].contents[0]))
                except IndexError:
                    print "Doesn't have a lawmaker. Probably a bad field."
                    
                try:
                    e, created = Earmark.objects.get_or_create(
                        tracking_number = tracking_number,
                        lawmaker = lawmaker,
                        year = year,
                        title = title,
                        detail_url = detail_url,
                        line_number = line_number,
                        amount = amount
                    )
                    if created:
                        print "+ %s" % e
                    else:
                        print "* %s" % e
                except UnboundLocalError:
                    print "Couldn't save this one."
                
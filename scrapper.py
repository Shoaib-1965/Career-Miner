"""
Job Scraper for Indeed and Glassdoor - 2025 UC Version
Uses undetected-chromedriver to bypass Cloudflare
Educational purposes only - Review ToS before use
"""

import time
import random
import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import re
from datetime import datetime
import os

class JobScraper:
    def __init__(self, headless=False):
        """Initialize the scraper with undetected Chrome driver"""
        
        # ChromeDriver path
        chromedriver_path = r"C:\Users\Shoaib Altaf\Documents\job_scrapper\drivers\chromedriver.exe"
        
        # Chrome profile path (copied, not live)
        chrome_profile_path = r"C:\Users\Shoaib Altaf\Documents\job_scrapper\chrome_profile"
        
        # Verify ChromeDriver exists
        if not os.path.exists(chromedriver_path):
            raise FileNotFoundError(f"❌ ChromeDriver not found at: {chromedriver_path}")
        
        print(f"✓ ChromeDriver found: {chromedriver_path}")
        print(f"✓ Using Chrome profile: {chrome_profile_path}")
        
        # UC Options
        options = uc.ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_argument('--disable-notifications')
        
        if headless:
            options.add_argument('--headless=new')
        
        # Initialize undetected Chrome with profile
        self.driver = uc.Chrome(
            driver_executable_path=chromedriver_path,
            user_data_dir=chrome_profile_path,
            options=options,
            version_main=None  # Auto-detect Chrome version
        )
        
        self.wait = WebDriverWait(self.driver, 15)
        self.short_wait = WebDriverWait(self.driver, 5)
        self.jobs_data = []
        
        print("✓ Undetected Chrome opened successfully\n")
    
    def random_delay(self, min_seconds=2, max_seconds=5):
        """Add random delay to mimic human behavior"""
        time.sleep(random.uniform(min_seconds, max_seconds))
    
    def extract_email(self, text):
        """Extract email addresses from text"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return ', '.join(set(emails)) if emails else None
    
    def extract_phone(self, text):
        """Extract phone numbers from text"""
        phone_patterns = [
            r'\+92[\s-]?\d{3}[\s-]?\d{7}',
            r'0\d{3}[\s-]?\d{7}',
            r'\d{4}[\s-]?\d{7}',
            r'\(\d{3}\)\s*\d{3}[-\s]?\d{4}'
        ]
        phones = []
        for pattern in phone_patterns:
            found = re.findall(pattern, text)
            phones.extend(found)
        return ', '.join(set(phones)) if phones else None
    
    def close_popups(self):
        """Close common popups and modals"""
        popup_selectors = [
            "button[aria-label='Close']",
            "button.modal_closeIcon",
            ".react-modal-close",
            "button[data-test='close-modal']",
            "svg[data-test='close-button']",
            ".modal-close-button",
            "button.CloseButton",
            "button[aria-label='close']",
            ".icl-CloseButton"
        ]
        
        for selector in popup_selectors:
            try:
                close_btn = self.short_wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                )
                close_btn.click()
                self.random_delay(0.5, 1)
                print("    ✓ Closed popup")
            except:
                continue
    
    def scrape_indeed(self, job_title="Flutter Developer", location="Lahore", max_pages=3):
        """Scrape jobs from Indeed - UC Version"""
        print(f"\n{'='*60}")
        print(f"Starting Indeed scraping for: {job_title} in {location}")
        print(f"{'='*60}\n")
        
        try:
            # Build search URL
            base_url = "https://pk.indeed.com/jobs"
            search_url = f"{base_url}?q={job_title.replace(' ', '+')}&l={location.replace(' ', '+')}"
            
            self.driver.get(search_url)
            print("✓ Indeed page loaded - bypassing Cloudflare...")
            self.random_delay(5, 8)  # Wait for Cloudflare check
            
            # Close any popups
            self.close_popups()
            
            page_count = 0
            
            while page_count < max_pages:
                print(f"\nScraping Indeed page {page_count + 1}...")
                
                try:
                    # Updated selectors for 2025
                    job_cards_selectors = [
                        "div.job_seen_beacon",
                        "div.cardOutline",
                        "article.job_card",
                        "div[data-testid='job-card']",
                        "li.job_card",
                        "div.slider_item"
                    ]
                    
                    job_cards = None
                    for selector in job_cards_selectors:
                        try:
                            job_cards = self.wait.until(
                                EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
                            )
                            print(f"  ✓ Using selector: {selector}")
                            break
                        except:
                            continue
                    
                    if not job_cards:
                        print("  ✗ Could not find job cards with any known selector")
                        break
                    
                    print(f"  Found {len(job_cards)} job listings on this page")
                    
                    for idx, card in enumerate(job_cards, 1):
                        try:
                            print(f"  Processing job {idx}/{len(job_cards)}...")
                            
                            # Scroll to element
                            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", card)
                            self.random_delay(0.5, 1)
                            
                            # Click on job card
                            card.click()
                            self.random_delay(2, 3)
                            
                            job_data = {
                                'source': 'Indeed',
                                'job_title': None,
                                'company': None,
                                'location': location,
                                'experience': None,
                                'email': None,
                                'phone': None,
                                'company_website': None,
                                'job_url': self.driver.current_url,
                                'scraped_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            }
                            
                            # Extract job title
                            title_selectors = [
                                "h2.jobsearch-JobInfoHeader-title",
                                "h1.jobsearch-JobInfoHeader-title",
                                "h2[data-testid='jobsearch-JobInfoHeader-title']",
                                "span.jobsearch-JobInfoHeader-title-container",
                                "h1.icl-u-xs-mb--xs"
                            ]
                            for selector in title_selectors:
                                try:
                                    title_elem = self.driver.find_element(By.CSS_SELECTOR, selector)
                                    job_data['job_title'] = title_elem.text.strip()
                                    break
                                except:
                                    continue
                            
                            # Extract company name
                            company_selectors = [
                                "[data-testid='inlineHeader-companyName']",
                                "[data-company-name='true']",
                                "div[data-testid='company-name']",
                                "a[data-testid='company-name']",
                                "span.companyName",
                                "div.icl-u-lg-mr--sm"
                            ]
                            for selector in company_selectors:
                                try:
                                    company_elem = self.driver.find_element(By.CSS_SELECTOR, selector)
                                    job_data['company'] = company_elem.text.strip()
                                    break
                                except:
                                    continue
                            
                            # Extract full job description
                            desc_selectors = [
                                "#jobDescriptionText",
                                "div.jobsearch-jobDescriptionText",
                                "[data-testid='job-description']",
                                "div.jobsearch-JobComponent-description"
                            ]
                            description = ""
                            for selector in desc_selectors:
                                try:
                                    desc_elem = self.driver.find_element(By.CSS_SELECTOR, selector)
                                    description = desc_elem.text
                                    break
                                except:
                                    continue
                            
                            if description:
                                job_data['email'] = self.extract_email(description)
                                job_data['phone'] = self.extract_phone(description)
                                
                                # Extract experience
                                exp_patterns = [
                                    r'(\d+[\+]?\s*(?:-\s*\d+)?\s*years?)',
                                    r'(\d+[\+]?\s*(?:to\s+\d+)?\s*years?)',
                                    r'experience:\s*(\d+[\+]?\s*(?:-\s*\d+)?\s*years?)'
                                ]
                                for pattern in exp_patterns:
                                    exp_match = re.search(pattern, description, re.IGNORECASE)
                                    if exp_match:
                                        job_data['experience'] = exp_match.group(1).strip()
                                        break
                            
                            self.jobs_data.append(job_data)
                            print(f"    ✓ Extracted: {job_data['job_title']} at {job_data['company']}")
                            if job_data['email']:
                                print(f"      📧 Email: {job_data['email']}")
                            if job_data['phone']:
                                print(f"      📞 Phone: {job_data['phone']}")
                            
                        except Exception as e:
                            print(f"    ✗ Error processing job: {str(e)}")
                            continue
                    
                    # Try to go to next page
                    try:
                        next_selectors = [
                            "[data-testid='pagination-page-next']",
                            "a[aria-label='Next Page']",
                            "a[data-testid='pagination-page-next']",
                            "a.np"
                        ]
                        for selector in next_selectors:
                            try:
                                next_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                                self.driver.execute_script("arguments[0].scrollIntoView();", next_button)
                                self.random_delay(1, 2)
                                next_button.click()
                                self.random_delay(3, 5)
                                page_count += 1
                                break
                            except:
                                continue
                        else:
                            print("  No more pages available")
                            break
                    except Exception as e:
                        print(f"  Pagination error: {str(e)}")
                        break
                        
                except TimeoutException:
                    print("  Timeout waiting for job listings")
                    break
                    
        except Exception as e:
            print(f"❌ Error during Indeed scraping: {str(e)}")
    
    def scrape_glassdoor(self, job_title="Flutter Developer", location="Lahore", max_pages=3):
        """Scrape jobs from Glassdoor - UC Version with manual search"""
        print(f"\n{'='*60}")
        print(f"Starting Glassdoor scraping for: {job_title} in {location}")
        print(f"{'='*60}\n")
        
        try:
            # Go to Glassdoor homepage first
            self.driver.get("https://www.glassdoor.com")
            print("✓ Glassdoor homepage loaded - bypassing Cloudflare...")
            self.random_delay(5, 8)
            
            # Close popups
            self.close_popups()
            
            # Find and fill job title search box
            try:
                job_search_selectors = [
                    "input#searchBar-jobTitle",
                    "input[name='sc.keyword']",
                    "input[placeholder*='Job title']",
                    "input[data-test='job-search-bar-input']"
                ]
                
                job_input = None
                for selector in job_search_selectors:
                    try:
                        job_input = self.wait.until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                        )
                        print(f"  ✓ Found job search box: {selector}")
                        break
                    except:
                        continue
                
                if job_input:
                    job_input.clear()
                    job_input.send_keys(job_title)
                    self.random_delay(1, 2)
                    print(f"  ✓ Entered job title: {job_title}")
                
            except Exception as e:
                print(f"  ⚠️ Could not enter job title: {str(e)}")
            
            # Find and fill location search box
            try:
                location_search_selectors = [
                    "input#searchBar-location",
                    "input[name='sc.location']",
                    "input[placeholder*='Location']",
                    "input[data-test='location-search-bar-input']"
                ]
                
                location_input = None
                for selector in location_search_selectors:
                    try:
                        location_input = self.driver.find_element(By.CSS_SELECTOR, selector)
                        print(f"  ✓ Found location box: {selector}")
                        break
                    except:
                        continue
                
                if location_input:
                    location_input.clear()
                    self.random_delay(0.5, 1)
                    location_input.send_keys(location)
                    self.random_delay(2, 3)  # Wait for autocomplete
                    print(f"  ✓ Entered location: {location}")
                    
                    # Press Enter or click first suggestion
                    from selenium.webdriver.common.keys import Keys
                    location_input.send_keys(Keys.RETURN)
                    print("  ✓ Submitted search")
                    
            except Exception as e:
                print(f"  ⚠️ Could not enter location: {str(e)}")
            
            self.random_delay(5, 8)  # Wait for results to load
            
            # Handle multiple popups
            self.close_popups()
            self.random_delay(1, 2)
            self.close_popups()
            
            page_count = 0
            
            while page_count < max_pages:
                print(f"\nScraping Glassdoor page {page_count + 1}...")
                
                try:
                    # Updated selector for 2025
                    job_cards = self.wait.until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article[data-test='job-card']"))
                    )
                    
                    print(f"  Found {len(job_cards)} job listings on this page")
                    
                    for idx, card in enumerate(job_cards, 1):
                        try:
                            print(f"  Processing job {idx}/{len(job_cards)}...")
                            
                            # Scroll to card
                            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", card)
                            self.random_delay(1, 2)
                            
                            # Click on job card
                            card.click()
                            self.random_delay(2, 4)
                            
                            # Close any new popups
                            self.close_popups()
                            
                            job_data = {
                                'source': 'Glassdoor',
                                'job_title': None,
                                'company': None,
                                'location': location,
                                'experience': None,
                                'email': None,
                                'phone': None,
                                'company_website': None,
                                'job_url': self.driver.current_url,
                                'scraped_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            }
                            
                            # Extract from card
                            try:
                                title_elem = card.find_element(By.CSS_SELECTOR, "[data-test='job-title']")
                                job_data['job_title'] = title_elem.text.strip()
                            except:
                                pass
                            
                            try:
                                company_elem = card.find_element(By.CSS_SELECTOR, "[data-test='employer-name']")
                                job_data['company'] = company_elem.text.strip()
                            except:
                                pass
                            
                            # Wait for description panel
                            desc_selectors = [
                                "[data-test='jobDescriptionContent']",
                                "div.JobDetails_jobDescription__uW_fK",
                                "div[class*='jobDescriptionContent']",
                                "div.desc",
                                "div[class*='JobDescription']"
                            ]
                            
                            description = ""
                            for selector in desc_selectors:
                                try:
                                    desc_elem = self.wait.until(
                                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                                    )
                                    description = desc_elem.text
                                    break
                                except:
                                    continue
                            
                            if description:
                                job_data['email'] = self.extract_email(description)
                                job_data['phone'] = self.extract_phone(description)
                                
                                # Extract experience
                                if 'year' in description.lower():
                                    exp_match = re.search(r'(\d+[\+]?\s*(?:-\s*\d+)?\s*years?)', description, re.IGNORECASE)
                                    if exp_match:
                                        job_data['experience'] = exp_match.group(1).strip()
                            
                            self.jobs_data.append(job_data)
                            print(f"    ✓ Extracted: {job_data['job_title']} at {job_data['company']}")
                            if job_data['email']:
                                print(f"      📧 Email: {job_data['email']}")
                            if job_data['phone']:
                                print(f"      📞 Phone: {job_data['phone']}")
                            
                        except Exception as e:
                            print(f"    ✗ Error processing job: {str(e)}")
                            continue
                    
                    # Try pagination
                    try:
                        next_button = self.driver.find_element(By.CSS_SELECTOR, "button[data-test='pagination-next']")
                        if next_button.is_enabled():
                            self.driver.execute_script("arguments[0].scrollIntoView();", next_button)
                            self.random_delay(1, 2)
                            next_button.click()
                            self.random_delay(4, 6)
                            page_count += 1
                        else:
                            print("  Next button disabled - no more pages")
                            break
                    except NoSuchElementException:
                        print("  No more pages available")
                        break
                        
                except TimeoutException:
                    print("  Timeout waiting for job listings")
                    break
                    
        except Exception as e:
            print(f"❌ Error during Glassdoor scraping: {str(e)}")
    
    def save_to_excel(self, filename="job_listings.xlsx"):
        """Save collected data to Excel file"""
        if not self.jobs_data:
            print("\n⚠️ No data to save!")
            return
        
        df = pd.DataFrame(self.jobs_data)
        
        # Reorder columns
        column_order = [
            'source', 'job_title', 'company', 'location', 
            'experience', 'email', 'phone', 'company_website', 
            'job_url', 'scraped_date'
        ]
        df = df[column_order]
        
        # Save to Excel
        df.to_excel(filename, index=False, engine='openpyxl')
        print(f"\n{'='*60}")
        print(f"✓ Data saved to {filename}")
        print(f"  Total jobs scraped: {len(self.jobs_data)}")
        print(f"  Indeed jobs: {len([j for j in self.jobs_data if j['source'] == 'Indeed'])}")
        print(f"  Glassdoor jobs: {len([j for j in self.jobs_data if j['source'] == 'Glassdoor'])}")
        print(f"  Jobs with email: {len([j for j in self.jobs_data if j['email']])}")
        print(f"  Jobs with phone: {len([j for j in self.jobs_data if j['phone']])}")
        print(f"{'='*60}\n")
    
    def close(self):
        """Close the browser"""
        self.driver.quit()


def main():
    """Main execution function"""
    print("\n" + "="*60)
    print("JOB SCRAPER - UC VERSION (Cloudflare Bypass)")
    print("Educational purposes only - Ensure ToS compliance")
    print("="*60 + "\n")
    
    # Configuration
    JOB_TITLE = "Flutter Developer"
    LOCATION = "Lahore"
    MAX_PAGES = 2
    
    print("⚠️  First time? You'll need to login to Indeed/Glassdoor manually once.")
    print("    After that, sessions are saved in chrome_profile folder.")
    print("\nPress Enter to continue...")
    input()
    
    # Initialize scraper
    scraper = JobScraper(headless=False)
    
    try:
        # Scrape Indeed
        scraper.scrape_indeed(job_title=JOB_TITLE, location=LOCATION, max_pages=MAX_PAGES)
        
        # Delay between sites
        print("\n" + "="*60)
        print("Waiting before switching to Glassdoor...")
        print("="*60)
        scraper.random_delay(5, 8)
        
        # Scrape Glassdoor
        scraper.scrape_glassdoor(job_title=JOB_TITLE, location=LOCATION, max_pages=MAX_PAGES)
        
        # Save results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_folder = r"C:\Users\Shoaib Altaf\Downloads"
        filename = os.path.join(output_folder, f"flutter_jobs_lahore_{timestamp}.xlsx")
        scraper.save_to_excel(filename)
        
        print(f"\n✓ Complete! Check your Downloads folder for the Excel file.")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Scraping interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error during scraping: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        scraper.close()
        print("\n✓ Browser closed. Scraping complete.")
        input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
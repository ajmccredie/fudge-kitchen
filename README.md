# Roo's Fudge Kitchen


## Project Rationale
A site for the e-commerce store selling homemade fudge. The site allows for products to be filtered according to allergen needs.
If you want to test the payment system, use these test card details:
Card Number: 4242 4242 4242 4242
Date: 0424
CVC: 242
Postcode: 42424


### Target audience:

## Business and customer goals
### User goals:
Purpose and value
### Business goals:
Purpose and value

### User stories and project goals
(potentially in a separate file, definitely in a table) - brief overview and covered in more detail later

## UX/UI
### Wireframes
(tablulate?)
### Colour schemes

### Fonts

### Mock-ups

### Design development and consistency in site theming

### Structure Plane: Key site features
#### Home page
#### Contact page
#### Main nav menu
#### Search bar
#### Site filtering
#### Subscriptions page
#### Edible products
#### Merchandise products
#### Product detail page
#### Restricted pages
#### Accounts pages (including sign-up, sign-in and sign-out)
#### Basket
#### Checkout
#### Admin dashboard features
#### Future features

## Data relationships
### ERD


## Marketing
### Business model

### Core business intent

### Search Engine Optimisation (SEO)
#### Keywords
{details about how the keywords on the site are anaylised and added to the description of the online store on the main page…}
#### SiteMap
{XML-Sitemaps creator – use on live site and place the XML created in the root directory of the website}
#### Robots
{create a robots.txt file to determine what should be looked at in SEO}


### Social media
#### Facebook business page (mockup)
Facebook business pages are used to allow followers to see and share up to date information about the brands that interest them. The page is used to inform about new products and promotions, place targeted advertising and to link users to the main product site.
#### Instagram with merchandise
Humorous merchandise and pictures with people and their bought products are encouraged in the delivery notes. The main aim of this is to generate interest in the brand and encourage people to visit the main page and make their own purchases.


### Newsletters
Users sign up with an email address. Those who do not opt out of marketing will receive emails detailing flavours of the month and other new and exciting products. 
This process is managed by {XXX}, and site users who have not yet signed


## Full user stories and acceptance criteria

## Manual testing (overview)
### Responsiveness

### Browser compatability

### Bugs
#### Resolved
#### Unresolved

### Lighthouse outcomes

### User stories tests

### Features tests

## Technologies used
### Frameworks
### Libraries
### Programmes

## References and credits

## Procedures
### Prerequisites and installs
1. An AWS account
2. A Django project ready for deployment
3. A Heroku account with your Django app successfully deployed (details of how to do this are shown below if you are unsure)


### Forking and cloning
#### Cloning the Project

This section guides you through the process of cloning this project to your local environment.

1. **Access the Repository**:
   - Go to the main page of the repository on GitHub.com.

2. **Copy the Repository URL**:
   - Click the ‘Code’ button located above the file list.
   - Choose your preferred clone method: HTTPS, SSH, or GitHub CLI.
   - Use the clipboard icon to copy the repository URL.

3. **Clone the Repository**:
   - Open your terminal.
   - Navigate to the directory where you want the cloned repository to be placed.
   - Type `git clone`, followed by a space, and then paste the URL you copied earlier.
   - Press Enter to execute the command and clone the repository.

#### Forking the Project

Forking the project allows you to freely experiment with changes without affecting the original project.

1. **Navigate to the Repository**:
   - Visit the main page of the repository on GitHub.

2. **Create a Fork**:
   - At the top-right corner of the page, find and click the "Fork" button.
   - This action will create a copy of the repository in your GitHub account.

3. **Clone Your Fork**:
   - Once the fork is created, you'll be redirected to your forked repository on GitHub.
   - Follow the same steps as cloning (outlined above) to clone your fork to your local machine.
   - Ensure you use the URL of your fork when performing the `git clone` command.

Both cloning and forking provide ways to interact with the project, whether you’re contributing directly or experimenting with your own version.

### Heroku App creation
1. **Disable Debug Mode**:
   - Ensure that debug mode is set to 'False' in your Django main app's `settings.py`.

2. **Install and Configure WhiteNoise**:
   - Install WhiteNoise using `pip3 install whitenoise`.
   - Add `'whitenoise.middleware.WhiteNoiseMiddleware'` to the `MIDDLEWARE` list in `settings.py`.
   - Configure static files in `settings.py`:
     ```python
     STATIC_URL = '/static/'
     STATIC_ROOT = BASE_DIR / 'staticfiles'
     STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
     ```

3. **Manage Static Files and Media**:
   - Check in the CSS file if any static images are called from your directory.
   - For each image, upload the file to an AWS S3 bucket and extract the direct link to the image.
   - Replace your image URLs in the CSS file with these S3 bucket links.

4. **Create a New Heroku App**:
   - Log in to your Heroku account and create a new app with a unique name in the appropriate region.

5. **Configure Host Settings**:
   - Copy the link for the deployed site from Heroku Domains (found under the 'settings' link in Heroku).
   - Ensure this link is added to `ALLOWED_HOSTS` in `settings.py`.

6. **Set Configuration Variables**:
   - In the app's 'Settings' tab, navigate to 'Config Vars' and add:
     - `PORT` with the value 8000.
     - Database credentials (e.g., `DATABASE_URL` for PostgreSQL).
     - `AWS_STORAGE_BUCKET_NAME` with your S3 bucket name.
     - Your `SECRET_KEY`.
     - `CLOUDINARY_URL` with your Cloudinary credentials for other media and image management needs.

7. **Update Requirements File**:
   - Back in your code editor, run `pip3 freeze > requirements.txt` to save project dependencies.

8. **Push Code to GitHub**:
   - Ensure all code changes are committed and pushed to GitHub.

9. **Configure Buildpacks on Heroku**:
   - In 'Buildpacks', add 'Python' and 'Node.js', ensuring Python is listed first.

10. **Deploy the Application**:
    - In the 'Deploy' tab, choose 'GitHub' as the deployment method.
    - Connect your GitHub account and select your repository.
    - Choose between automatic or manual deployment.

11. **Post-Deployment Testing**:
    - After deployment, extensively test the project to ensure it behaves as expected, particularly focusing on static and media file accessibility from AWS S3.

### AWS S3 Bucket Creation and set-up
AWS S3 is used to store static and media files, as Heroku does not persist this type of data after the dyno restarts.

#### Step 1: Creating an S3 Bucket

- Log in to your AWS Management Console.
- Navigate to the S3 service.
- Click "Create bucket".
  - **Bucket name**: Choose a name, ideally matching your Heroku app's name.
  - **Region**: Select the region closest to you.
  - **Uncheck** "Block all public access" and acknowledge that the bucket will be public.
  - Under "Object Ownership", enable ACLs and select "Bucket owner preferred".
  - In the "Properties" tab, enable static website hosting. Set "index.html" and "error.html" as the default documents.

#### Step 2: Setting Permissions

- Go to the "Permissions" tab of your bucket.
- **CORS Configuration**: Add the following CORS configuration:
  ```json
  [
      {
          "AllowedHeaders": ["Authorization"],
          "AllowedMethods": ["GET"],
          "AllowedOrigins": ["*"],
          "ExposeHeaders": []
      }
  ]

#### Step 3: Configuring Bucket Policy

- Go to the "Bucket Policy" tab within your bucket settings.
- Use the Policy Generator to create a policy:
  - **Policy Type**: S3 Bucket Policy
  - **Effect**: Allow
  - **Principal**: "*"
  - **Action**: "GetObject"
  - **Amazon Resource Name (ARN)**: Paste your bucket ARN here
- Click "Add Statement" then "Generate Policy" and copy the generated policy.
- Paste the copied policy into the bucket policy editor. Ensure the policy looks like this, replacing `your-bucket-name` with your actual bucket name:
  ```json
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Sid": "AllowPublicReadAccess",
        "Effect": "Allow",
        "Principal": "*",
        "Action": "s3:GetObject",
        "Resource": "arn:aws:s3:::your-bucket-name/*"
      }
    ]
  }

#### Step 4: IAM Setup for Access Control

- Navigate back to the AWS Management Console home and select IAM (Identity and Access Management).
- **Creating User Groups**:
  - Click "User Groups" then "Create New Group".
  - Name your group `group-your-project-name`.
  - After creating the group, attach the `AmazonS3FullAccess` policy to it.
- **Creating Users**:
  - In the IAM dashboard, click "Users" and then "Add user".
  - Enter a user name like `user-your-project-name`.
  - Select "Programmatic access" as the access type.
  - Add the user to the group `group-your-project-name`.
  - Complete the user creation and download the .csv file containing the Access key ID and Secret access key. Make sure to store this file securely as it cannot be downloaded again.

### Integrating AWS S3 with Django

- Include `boto3` and `django-storages` in your project by adding them to your `requirements.txt` file.
- Configure your Django settings to use AWS S3 for serving static and media files:
  ```python
  AWS_STORAGE_BUCKET_NAME = 'your-bucket-name'
  AWS_S3_REGION_NAME = 'your-region'
  AWS_ACCESS_KEY_ID = 'your-access-key-id-from-csv'
  AWS_SECRET_ACCESS_KEY = 'your-secret-access-key-from-csv'
  AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

  # settings for static files
  STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
  STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

  # settings for media files
  DEFAULT_FILE_STORAGE = 'your_project_name.storage_backends.MediaStorage'
  MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'

#### Configuring Heroku

- On your Heroku dashboard, navigate to your application's settings.
- In the "Config Vars" section, ensure that the following are set:
  - `AWS_STORAGE_BUCKET_NAME`
  - `AWS_S3_REGION_NAME`
  - `AWS_ACCESS_KEY_ID`
  - `AWS_SECRET_ACCESS_KEY`
- Remove the `DISABLE_COLLECTSTATIC` config var if it exists, to allow Django to manage static files effectively.
- Confirm all environment variables are correctly configured to align with your AWS and Django settings.

#### Finalizing Setup

- Push your changes to Heroku using:
  ```bash
  git push heroku master
- Verify that static and media files are being served correctly from your S3 bucket by visiting your application and checking that all assets load properly.
- Monitor the Heroku logs for any errors during deployment or while accessing the files to ensure everything is functioning as expected.

### Stripe configuration
This project uses Stripe for processing ecommerce payments efficiently.

### Setting Up Stripe

1. **Create and Configure Your Stripe Account**:
   - Sign up or log into your Stripe account.

2. **Retrieve API Keys**:
   - Navigate to your Stripe dashboard.
   - Expand the "Get your test API keys" section.
   - Note down your keys:
     - `STRIPE_PUBLIC_KEY` = Publishable Key (begins with `pk`)
     - `STRIPE_SECRET_KEY` = Secret Key (begins with `sk`)

#### Configuring Stripe Webhooks

To ensure seamless transaction processing, especially if users exit the purchase-order page prematurely, setting up webhooks is crucial.

1. **Set Up Webhooks**:
   - In your Stripe dashboard, go to the "Developers" section and select "Webhooks".
   - Click "Add Endpoint" and enter your endpoint URL:
     ```
     https://[your-deployed-site].herokuapp.com/checkout/wh/
     ```
   - Choose to receive all events.
   - Click "Add Endpoint" to finalize the setup.

2. **Webhook Signing Secret**:
   - After adding the endpoint, you will receive a new key:
     - `STRIPE_WH_SECRET` = Signing Secret (Webhook Key, starts with `wh`)

#### Final Steps

Ensure that all Stripe keys are securely stored and correctly configured in your project settings to facilitate transactions. Test the webhook by simulating payments to verify that the integration works as expected.
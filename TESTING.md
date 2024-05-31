# Full details of manual site testing
## Site browser compatability
The site was checked for compatability on Chrome, Edge and Firefox

## Home page
| Test case description  | Expected outcome |  Pass?  | 
| ----------- | ----------- | ----------- |
| User navigation | User can see and access available options | Yes  |

|  HTML  |  CSS  |  JSHint  |  Python Linter  |  Lighthouse |
| ---- | ---- | ---- | ---- | ---- |
| ![Home HTML](static/images/READMEImages/index-html-checked.png) | ![CSS validation](static/images/READMEImages/css-validated.png) | N/A | No issues | ![Home Lighthouse](static/images/READMEImages/Lighthouse-home.png) |


#### Main nav menu
| Test case description  | Expected outcome |  Pass?  | 
| ----------- | ----------- | ----------- |
| User navigation | User can access any required part of the site | Yes  |
| User profile access | User can access login or sign up options. Logged in users can access account details. | Yes |
| Basket view and access | Users can see toasts with details, and a running total under their basket in the corner at all times | Yes |

#### Search bar
| Form field  | Blank |  Too long/large  |  Incorrect  | Invalid |
| ----------- | ----------- | ----------- | ----------- | --------|
| Text entry | Results show no results available for " " |  | Spelling mistakes are unlikely to generate zero results. | N/A |

Page returning general search results
|  HTML  |  CSS  |  JSHint  |  Python Linter  |  Lighthouse |
| ---- | ---- | ---- | ---- | ---- |
| ![Search results HTML](static/images/READMEImages/search-html-checked.png) | ![CSS validation](static/images/READMEImages/css-validated.png) | N/A | No issues | ![Search results Lighthouse](static/images/READMEImages/Lighthouse-search.png)  |

#### Other tests of possible user actions
| Action description  | Result acceptable? | 
| ----------- | ----------- |
| Back-up |  Browser back-up in Chrome not supported from this page. |
| Navigating elsewhere |  No issues found |
| Page reload |  Search results maintained |

[Return to Top](#full-details-of-manual-site-testing)

## About us
| Test case description  | Expected outcome |  Pass?  | 
| ----------- | ----------- | ----------- |
| Read story | Story renders on page and can be read | Yes  |
| View images | Images render with the story and can be seen | Yes  |
| Navigate to inquiries and FAQs | Links work and navigate to the expected page | Yes |
| Views FAQs | Each FAQ will drop open when clicked and remain open until clicked again | Yes |
| Non-signed in users cannot access inquiries | This part demands a login or sign-up if the user is not already authenticated | Yes |
| Signed in users can access inquiries | The form and submit button render if the user is authenticated | Yes |
| User feedback on actions | Users receive a confirmation toast when they send an inquiry | Yes |

Our Story
|  HTML  |  CSS  |  JSHint  |  Python Linter  |  Lighthouse |
| ---- | ---- | ---- | ---- | ---- |
| [Our Story HTML](static/images/READMEImages/story-html-checked.png) | ![CSS validation](static/images/READMEImages/css-validated.png) | N/A | no issues | [Story Lighthouse](static/images/READMEImages/Lighthouse-ourstory.png) |

FAQs and Contact Us
|  HTML  |  CSS  |  JSHint  |  Python Linter  |  Lighthouse |
| ---- | ---- | ---- | ---- | ---- |
| ![FAQ HTML](static/images/READMEImages/faq-html-checked.png) | ![CSS validation](static/images/READMEImages/css-validated.png) |  |  |  |

#### Restricted pages
| Test case description  | Expected outcome |  Pass?  | 
| ----------- | ----------- | ----------- |
| Only signed-in users access the inquiries form | Users are directed to login or sign-up. A new sign-up will have their email verified. Redirects to page with the form. Logged in users can use the form | Yes  |

#### Other tests of possible user actions
| Action description  | Result acceptable? | 
| ----------- | ----------- |
|  |   |

[Return to Top](#full-details-of-manual-site-testing)

## Edible Products
| Test case description  | Expected outcome |  Pass?  | 
| ----------- | ----------- | ----------- |
| Display all products | Products display with correct price and images, and link to the correct product details |   |
| Products displayed according to preference | Products can be correctly displayed as 'All', 'Plant-based' or 'Traditional' | Yes |
| Allergen filtering | Products can be filtered on page according to selected allergens, and this can be changed multiple times without issue. | Yes |
| Guest products are identifiable | Guest products are shown with a banner which states they are 'guest products' | Yes |

|  HTML  |  CSS  |  JSHint  |  Python Linter  |  Lighthouse |
| ---- | ---- | ---- | ---- | ---- |
|  | ![CSS validation](static/images/READMEImages/css-validated.png) |  |  |  |

#### Edible product detail page
| Test case description  | Expected outcome |  Pass?  | 
| ----------- | ----------- | ----------- |
|  |  |   |

|  HTML  |  CSS  |  JSHint  |  Python Linter  |  Lighthouse |
| ---- | ---- | ---- | ---- | ---- |
|  | ![CSS validation](static/images/READMEImages/css-validated.png) |  |  |  |

| Form field  | Blank |  Too long/large  |  Incorrect  | Invalid |
| ----------- | ----------- | ----------- | ----------- | --------|
| Choice of weight and price |  |  |  |  |
| Number of products to add |  |  |  |  |


#### Site filtering
| Test case description  | Expected outcome |  Pass?  | 
| ----------- | ----------- | ----------- |
|  |  |   |


#### Other tests of possible user actions
| Action description  | Result acceptable? | 
| ----------- | ----------- |
|  |   |

[Return to Top](#full-details-of-manual-site-testing)

## Merchandise products
| Test case description  | Expected outcome |  Pass?  | 
| ----------- | ----------- | ----------- |
| Product list display | Products display with correct name and image, and are a link to a page with the details for that product |   |

|  HTML  |  CSS  |  JSHint  |  Python Linter  |  Lighthouse |
| ---- | ---- | ---- | ---- | ---- |
|  | ![CSS validation](static/images/READMEImages/css-validated.png) |  |  |  |

#### Merch product detail page
| Test case description  | Expected outcome |  Pass?  | 
| ----------- | ----------- | ----------- |
| Product details display with correct image |  |   |
| Product selection | Product in volume of 1-99 can be added to basket and appears correctly in toast  | Yes |
| Links to alternative colours | Alternative colours, where available, are displayed and are links to that product detail page instead | Yes |

|  HTML  |  CSS  |  JSHint  |  Python Linter  |  Lighthouse |
| ---- | ---- | ---- | ---- | ---- |
|  | ![CSS validation](static/images/READMEImages/css-validated.png) |  |  |  |

| Form field  | Blank |  Too long/large  |  Incorrect  | Invalid |
| ----------- | ----------- | ----------- | ----------- | --------|
| Text choice |  |  |  |  |
| Number to add to basket |  |  |  |  |

#### Other tests of possible user actions
| Action description  | Result acceptable? | 
| ----------- | ----------- |
|  |   |

[Return to Top](#full-details-of-manual-site-testing)

## Accounts pages (including sign-up, sign-in and sign-out)
| Test case description  | Expected outcome |  Pass?  | 
| ----------- | ----------- | ----------- |
|  User registration |  |   |
| User login |  |  |

|  HTML  |  CSS  |  JSHint  |  Python Linter  |  Lighthouse |
| ---- | ---- | ---- | ---- | ---- |
|  | ![CSS validation](static/images/READMEImages/css-validated.png) |  |  |  |

| Form field  | Blank |  Too long/large  |  Incorrect  | Invalid |
| ----------- | ----------- | ----------- | ----------- | --------|
| Username |  |  |  |  |
| Email |  |  |  |  |
| Password |  |  |  |  |

#### Other tests of possible user actions
| Action description  | Result acceptable? | 
| ----------- | ----------- |
|  |   |

#### Basket
| Test case description  | Expected outcome |  Pass?  | 
| ----------- | ----------- | ----------- |
| Subscription status honoured | If a user is already a subscriber, this is reflected in the banner and the removal of the delivery charge. If the subscription product is in the basket for checkout, the same thing happens. | Yes  |
|  |  |   |

|  HTML  |  CSS  |  JSHint  |  Python Linter  |  Lighthouse |
| ---- | ---- | ---- | ---- | ---- |
| Two warnings, but function of page is not impacted <br> ![Basket HTML Vadlidated](static/images/READMEImages/basket-html-checked.png) | ![CSS validation](static/images/READMEImages/css-validated.png) | ![JShint validation](static/images/READMEImages/jshint-basket.png) | One variable in a 'try/except' statement showing as unused. | The basket can only be checked as empty: <br> ![Lighthouse Basket](static/images/READMEImages/Lighthouse-basket.png) |

| Form field  | Blank |  Too long/large  |  Incorrect  | Invalid |
| ----------- | ----------- | ----------- | ----------- | --------|
| Number of products |  |  |  |  |
| Update |  |  |  |  |
| Remove |  |  |  |  |
| Increment up/down |  |  |  |  |

#### Other tests of possible user actions
| Action description  | Result acceptable? | 
| ----------- | ----------- |
| Adding multiple increments of 99 products to basket | These products are all added, although this might prove difficult for the business, all products are charged for, so fulfilling the order might actually be lucrative. Result is acceptable.  |
| User empties all items from basket | Empty basket with the option to 'Keep shopping' returned. Result acceptable.  |

#### Checkout
| Test case description  | Expected outcome |  Pass?  | 
| ----------- | ----------- | ----------- |
| User can view their products | Products and details display, with the option to return to the basket if anything is incorrect | Yes  |
| Subscription status honoured | If a user is already a subscriber, this is reflected in the banner and the removal of the delivery charge. If the subscription product is in the basket for checkout, the same thing happens. | Yes  |
| Update address as required | All fields can be altered with the exception of the email address | Yes |
| Complete checkout | Customer can checkout, receive a confirmation toast and a confirmation email on click (if all form fields are valid) | Yes |


|  HTML  |  CSS  |  JSHint  |  Python Linter  |  Lighthouse |
| ---- | ---- | ---- | ---- | ---- |
| Cannot be checked because login protected | ![CSS validation](static/images/READMEImages/css-validated.png) | Some errors of unused variables, largely taken through walkthrough code. <br> ![JSHint Checkout](static/images/READMEImages/jshint-checkout.png) | One line in the models and three in the webhook_handler exceed the character limit of 79 (the worst being 85 characters). | Cannot be checked because login protected |

| Form field  | Blank |  Too long/large  |  Incorrect  | Invalid |
| ----------- | ----------- | ----------- | ----------- | --------|
| Name | User prompted to enter | No further input allowed after charcter limit | Wrong name will be sent on order | Wrong name will be sent on order |
| Email | Cannot be deleted | Cannot be changed | Cannot be changed | Was verified on sign-up |
| Address Line 1 | User prompted to enter | No further input allowed after charcter limit | Wrong name will be sent on order. Depending on the error, it may or may not reach the destination, but the site cannot know if the address is valid or correct | Wrong name will be sent on order. Depending on the error, it may or may not reach the destination, but the site cannot know if the address is valid or correct |
| Address Line 2 (optional) | Order proceeds without issue | No further input allowed after charcter limit | No issue | No issue |
| Town/City | User prompted to enter | No further input allowed after charcter limit | Wrong name will be sent on order. Depending on the error, it may or may not reach the destination, but the site cannot know if the address is valid or correct | Wrong name will be sent on order. Depending on the error, it may or may not reach the destination, but the site cannot know if the address is valid or correct |
| County (optional) | Order proceeds without issue | No further input allowed after charcter limit | No issue | No issue |
| Country | User prompted to enter | No further input allowed after charcter limit | Drop down menu, so cannot be incorrect | Wrong country may be selected. If the rest of the address is correct, it shouldn't cause too much issue |
| Post code | Payment proceeds so long as it is entered in the Stripe element | No further input allowed after the character limit | The Stripe element will override |  The Stripe element will override |
| Stripe Payment | Tries to complete the payment, but returns to checkout page with message of card number being incomplete | Will not accept more digits | Returns to the checkout page with errors visible under the Stripe element | Returns to the checkout page with errors visible under the Stripe element |

The Stripe payments were tested using their set of test numbers. It was also confirmed that after the user received their error warning that they were then able to complete a purchase as planned with a correct number.



#### Other tests of possible user actions
| Action description  | Result acceptable? | 
| ----------- | ----------- |
| Back-up |   |
| Change page from a link |   |
| Change page from the page address bar |   |

#### Restricted pages
| Test case description  | Expected outcome |  Pass?  | 
| ----------- | ----------- | ----------- |
| User login |  |   |
| User logout |  |   |
| Store admin login |  |   |

| Form field  | Blank |  Too long/large  |  Incorrect  | Invalid |
| ----------- | ----------- | ----------- | ----------- | --------|
| Sign-up |  |  |  |  |
| Sign-in |  |  |  |  |
| Password |  |  |  |  |

#### Other tests of possible user actions
| Action description  | Result acceptable? | 
| ----------- | ----------- |
| Attempting access with the address bar |   |
| Back-up after logging out |   |

## Subscriptions page
| Test case description  | Expected outcome |  Pass?  | 
| ----------- | ----------- | ----------- |
| View non-restricted content when not registered/logged in |  |   |
| Access to restricted content after logging in |  |   |

|  HTML  |  CSS  |  JSHint  |  Python Linter  |  Lighthouse |
| ---- | ---- | ---- | ---- | ---- |
|  | ![CSS validation](static/images/READMEImages/css-validated.png) |  |  |  |

#### Other tests of possible user actions
| Action description  | Result acceptable? | 
| ----------- | ----------- |
| Attempt to register the same email address twice |   |

## Admin dashboard features
| Test case description  | Expected outcome |  Pass?  | 
| ----------- | ----------- | ----------- |
|  |  |   |

|  HTML  |  CSS  |  JSHint  |  Python Linter  |  Lighthouse |
| ---- | ---- | ---- | ---- | ---- |
|  | ![CSS validation](static/images/READMEImages/css-validated.png) |  |  |  |

### CRUD of Edible Products
| Test case description  | Expected outcome |  Pass?  | 
| ----------- | ----------- | ----------- |
|  |  |   |

|  HTML  |  CSS  |  JSHint  |  Python Linter  |  Lighthouse |
| ---- | ---- | ---- | ---- | ---- |
|  | ![CSS validation](static/images/READMEImages/css-validated.png) |  |  |  |

| Form field  | Blank |  Too long/large  |  Incorrect  | Invalid |
| ----------- | ----------- | ----------- | ----------- | --------|
|  |  |  |  |  |

### CRUD of Merch Products
| Test case description  | Expected outcome |  Pass?  | 
| ----------- | ----------- | ----------- |
|  |  |   |

|  HTML  |  CSS  |  JSHint  |  Python Linter  |  Lighthouse |
| ---- | ---- | ---- | ---- | ---- |
|  | ![CSS validation](static/images/READMEImages/css-validated.png) |  |  |  |

| Form field  | Blank |  Too long/large  |  Incorrect  | Invalid |
| ----------- | ----------- | ----------- | ----------- | --------|
|  |  |  |  |  |

### Tracking of orders
| Test case description  | Expected outcome |  Pass?  | 
| ----------- | ----------- | ----------- |
|  |  |   |

|  HTML  |  CSS  |  JSHint  |  Python Linter  |  Lighthouse |
| ---- | ---- | ---- | ---- | ---- |
|  | ![CSS validation](static/images/READMEImages/css-validated.png) |  |  |  |

| Form field  | Blank |  Too long/large  |  Incorrect  | Invalid |
| ----------- | ----------- | ----------- | ----------- | --------|
|  |  |  |  |  |

### Receiving and checking off inquiries
| Test case description  | Expected outcome |  Pass?  | 
| ----------- | ----------- | ----------- |
|  |  |   |

|  HTML  |  CSS  |  JSHint  |  Python Linter  |  Lighthouse |
| ---- | ---- | ---- | ---- | ---- |
|  | ![CSS validation](static/images/READMEImages/css-validated.png) |  |  |  |

| Form field  | Blank |  Too long/large  |  Incorrect  | Invalid |
| ----------- | ----------- | ----------- | ----------- | --------|
|  |  |  |  |  |


#### Other tests of possible user actions
| Action description  | Result acceptable? | 
| ----------- | ----------- |
|  |   |

## General testing of additional JavaScript files
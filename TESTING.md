# Full details of manual site testing
## Site browser compatability

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
|  | ![CSS validation](static/images/READMEImages/css-validated.png) |  |  |  |

FAQs and Contact Us
|  HTML  |  CSS  |  JSHint  |  Python Linter  |  Lighthouse |
| ---- | ---- | ---- | ---- | ---- |
| ![FAQ HTML](static/images/READMEImages/faq-html-checked.png) | ![CSS validation](static/images/READMEImages/css-validated.png) |  |  |  |

#### Restricted pages
| Test case description  | Expected outcome |  Pass?  | 
| ----------- | ----------- | ----------- |
| Only signed-in users access the inquiries form |  |   |

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

| Form field  | Blank |  Too long/large  |  Incorrect  | Invalid |
| ----------- | ----------- | ----------- | ----------- | --------|
| All edible products link |  |  |  |  |
| Plant-based edible products link |  |  |  |  |
| Traditional edible products link |  |  |  |  |
| Allergen filters |  |  |  |  |


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
|  |  |   |

|  HTML  |  CSS  |  JSHint  |  Python Linter  |  Lighthouse |
| ---- | ---- | ---- | ---- | ---- |
|  | ![CSS validation](static/images/READMEImages/css-validated.png) |  |  |  |

| Form field  | Blank |  Too long/large  |  Incorrect  | Invalid |
| ----------- | ----------- | ----------- | ----------- | --------|
| Number of products |  |  |  |  |
| Update |  |  |  |  |
| Remove |  |  |  |  |
| Increment up/down |  |  |  |  |

#### Other tests of possible user actions
| Action description  | Result acceptable? | 
| ----------- | ----------- |
|  |   |

#### Checkout
| Test case description  | Expected outcome |  Pass?  | 
| ----------- | ----------- | ----------- |
|  |  |   |

|  HTML  |  CSS  |  JSHint  |  Python Linter  |  Lighthouse |
| ---- | ---- | ---- | ---- | ---- |
|  | ![CSS validation](static/images/READMEImages/css-validated.png) |  |  |  |

| Form field  | Blank |  Too long/large  |  Incorrect  | Invalid |
| ----------- | ----------- | ----------- | ----------- | --------|
| Name |  |  |  |  |
| Email |  |  |  |  |
| Address Line 1 |  |  |  |  |
| Address Line 2 (optional) |  |  |  |  |
| Town/City |  |  |  |  |
| County (optional) |  |  |  |  |
| Country |  |  |  |  |
| Stripe Payment |  |  |  |  |

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
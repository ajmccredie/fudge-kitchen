# Full details of manual site testing
## Site browser compatability


## Home page
| Test case description  | Expected outcome |  Pass?  | 
| ----------- | ----------- | ----------- |
| User navigation | User can see and access available options | Yes  |

|  HTML  |  CSS  |  JSHint  |  Python Linter  |  Lighthouse |
| ---- | ---- | ---- | ---- | ---- |
| ![Home HTML](static/images/READMEImages/index-html-checked.png) | ![CSS validation](static/images/READMEImages/css-validated-html.png) |  |  | ![Home Lighthouse](static/images/READMEImages/Lighthouse-home.png) |


#### Main nav menu
| Test case description  | Expected outcome |  Pass?  | 
| ----------- | ----------- | ----------- |
| User navigation | User can access any required part of the site | Yes  |
| User profile access | User can access login or sign up options. Logged in users can access account details. | Yes |
| Basket view and access | Users can see toasts with details, and a running total under their basket in the corner at all times | Yes |

#### Search bar
| Form field  | Blank |  Too long/large  |  Incorrect  | Invalid |
| ----------- | ----------- | ----------- | ----------- | --------|
| Text entry |  |  |  |  |

Page returning general search results
|  HTML  |  CSS  |  JSHint  |  Python Linter  |  Lighthouse |
| ---- | ---- | ---- | ---- | ---- |
|  | ![CSS validation](static/images/READMEImages/css-validated-html.png) |  |  |  |

#### Other tests of possible user actions
| Action description  | Result acceptable? | 
| ----------- | ----------- |
|  |   |

## About us
| Test case description  | Expected outcome |  Pass?  | 
| ----------- | ----------- | ----------- |
| Read story |  |   |
| View images |  |   |
| Navigate to inquiries and FAQs |  |  |
| Views FAQs |  |  |
| Non-signed in users cannot access inquiries |  |  |
| Signed in users can access inquiries |  |  |

Our Story
|  HTML  |  CSS  |  JSHint  |  Python Linter  |  Lighthouse |
| ---- | ---- | ---- | ---- | ---- |
|  | ![CSS validation](static/images/READMEImages/css-validated-html.png) |  |  |  |

FAQs and Contact Us
|  HTML  |  CSS  |  JSHint  |  Python Linter  |  Lighthouse |
| ---- | ---- | ---- | ---- | ---- |
| ![FAQ HTML](static/images/READMEImages/faq-html-checked.png) | ![CSS validation](static/images/READMEImages/css-validated-html.png) |  |  |  |

#### Restricted pages
| Test case description  | Expected outcome |  Pass?  | 
| ----------- | ----------- | ----------- |
| Only signed-in users access the inquiries form |  |   |

#### Other tests of possible user actions
| Action description  | Result acceptable? | 
| ----------- | ----------- |
|  |   |

## Edible Products
| Test case description  | Expected outcome |  Pass?  | 
| ----------- | ----------- | ----------- |
| Display all products | Products display with correct price and images, and link to the correct product details |   |
| Products displayed according to preference | Products can be correctly displayed as 'All', 'Plant-based' or 'Traditional' | Yes |
| Allergen filtering | Products can be filtered on page according to selected allergens, and this can be changed multiple times without issue. | Yes |

|  HTML  |  CSS  |  JSHint  |  Python Linter  |  Lighthouse |
| ---- | ---- | ---- | ---- | ---- |
|  | ![CSS validation](static/images/READMEImages/css-validated-html.png) |  |  |  |

#### Edible product detail page
| Test case description  | Expected outcome |  Pass?  | 
| ----------- | ----------- | ----------- |
|  |  |   |

|  HTML  |  CSS  |  JSHint  |  Python Linter  |  Lighthouse |
| ---- | ---- | ---- | ---- | ---- |
|  | ![CSS validation](static/images/READMEImages/css-validated-html.png) |  |  |  |

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

## Merchandise products
| Test case description  | Expected outcome |  Pass?  | 
| ----------- | ----------- | ----------- |
| Product list display | Products display with correct name and image, and are a link to a page with the details for that product |   |

|  HTML  |  CSS  |  JSHint  |  Python Linter  |  Lighthouse |
| ---- | ---- | ---- | ---- | ---- |
|  | ![CSS validation](static/images/READMEImages/css-validated-html.png) |  |  |  |

#### Merch product detail page
| Test case description  | Expected outcome |  Pass?  | 
| ----------- | ----------- | ----------- |
| Product details display with correct image |  |   |
| Product selection | Product in volume of 1-99 can be added to basket and appears correctly in toast  | Yes |
| Links to alternative colours | Alternative colours, where available, are displayed and are links to that product detail page instead | Yes |

|  HTML  |  CSS  |  JSHint  |  Python Linter  |  Lighthouse |
| ---- | ---- | ---- | ---- | ---- |
|  | ![CSS validation](static/images/READMEImages/css-validated-html.png) |  |  |  |

| Form field  | Blank |  Too long/large  |  Incorrect  | Invalid |
| ----------- | ----------- | ----------- | ----------- | --------|
| Text choice |  |  |  |  |
| Number to add to basket |  |  |  |  |

#### Other tests of possible user actions
| Action description  | Result acceptable? | 
| ----------- | ----------- |
|  |   |

## Accounts pages (including sign-up, sign-in and sign-out)
| Test case description  | Expected outcome |  Pass?  | 
| ----------- | ----------- | ----------- |
|  User registration |  |   |
| User login |  |  |

|  HTML  |  CSS  |  JSHint  |  Python Linter  |  Lighthouse |
| ---- | ---- | ---- | ---- | ---- |
|  | ![CSS validation](static/images/READMEImages/css-validated-html.png) |  |  |  |

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
|  | ![CSS validation](static/images/READMEImages/css-validated-html.png) |  |  |  |

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
|  | ![CSS validation](static/images/READMEImages/css-validated-html.png) |  |  |  |

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
|  |   |

#### Restricted pages
| Test case description  | Expected outcome |  Pass?  | 
| ----------- | ----------- | ----------- |
|  |  |   |

| Form field  | Blank |  Too long/large  |  Incorrect  | Invalid |
| ----------- | ----------- | ----------- | ----------- | --------|
| Sign-up |  |  |  |  |
| Sign-in |  |  |  |  |

#### Other tests of possible user actions
| Action description  | Result acceptable? | 
| ----------- | ----------- |
|  |   |

## Subscriptions page
| Test case description  | Expected outcome |  Pass?  | 
| ----------- | ----------- | ----------- |
|  |  |   |

|  HTML  |  CSS  |  JSHint  |  Python Linter  |  Lighthouse |
| ---- | ---- | ---- | ---- | ---- |
|  | ![CSS validation](static/images/READMEImages/css-validated-html.png) |  |  |  |

#### Other tests of possible user actions
| Action description  | Result acceptable? | 
| ----------- | ----------- |
|  |   |

## Admin dashboard features
| Test case description  | Expected outcome |  Pass?  | 
| ----------- | ----------- | ----------- |
|  |  |   |

|  HTML  |  CSS  |  JSHint  |  Python Linter  |  Lighthouse |
| ---- | ---- | ---- | ---- | ---- |
|  | ![CSS validation](static/images/READMEImages/css-validated-html.png) |  |  |  |

### CRUD of Edible Products
| Test case description  | Expected outcome |  Pass?  | 
| ----------- | ----------- | ----------- |
|  |  |   |

|  HTML  |  CSS  |  JSHint  |  Python Linter  |  Lighthouse |
| ---- | ---- | ---- | ---- | ---- |
|  | ![CSS validation](static/images/READMEImages/css-validated-html.png) |  |  |  |

| Form field  | Blank |  Too long/large  |  Incorrect  | Invalid |
| ----------- | ----------- | ----------- | ----------- | --------|
|  |  |  |  |  |

### CRUD of Merch Products
| Test case description  | Expected outcome |  Pass?  | 
| ----------- | ----------- | ----------- |
|  |  |   |

|  HTML  |  CSS  |  JSHint  |  Python Linter  |  Lighthouse |
| ---- | ---- | ---- | ---- | ---- |
|  | ![CSS validation](static/images/READMEImages/css-validated-html.png) |  |  |  |

| Form field  | Blank |  Too long/large  |  Incorrect  | Invalid |
| ----------- | ----------- | ----------- | ----------- | --------|
|  |  |  |  |  |

### Tracking of orders
| Test case description  | Expected outcome |  Pass?  | 
| ----------- | ----------- | ----------- |
|  |  |   |

|  HTML  |  CSS  |  JSHint  |  Python Linter  |  Lighthouse |
| ---- | ---- | ---- | ---- | ---- |
|  | ![CSS validation](static/images/READMEImages/css-validated-html.png) |  |  |  |

| Form field  | Blank |  Too long/large  |  Incorrect  | Invalid |
| ----------- | ----------- | ----------- | ----------- | --------|
|  |  |  |  |  |

### Receiving and checking off inquiries
| Test case description  | Expected outcome |  Pass?  | 
| ----------- | ----------- | ----------- |
|  |  |   |

|  HTML  |  CSS  |  JSHint  |  Python Linter  |  Lighthouse |
| ---- | ---- | ---- | ---- | ---- |
|  | ![CSS validation](static/images/READMEImages/css-validated-html.png) |  |  |  |

| Form field  | Blank |  Too long/large  |  Incorrect  | Invalid |
| ----------- | ----------- | ----------- | ----------- | --------|
|  |  |  |  |  |


#### Other tests of possible user actions
| Action description  | Result acceptable? | 
| ----------- | ----------- |
|  |   |

## General testing of additional JavaScript files
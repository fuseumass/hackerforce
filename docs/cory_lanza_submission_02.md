# Cory Lanza
## Data Model
I drew out the rough draft of our overall data model, which was used as a guide to create our data model in Django.
![alt text](https://github.com/326-queue/project/blob/development/docs/imgs/data_model_rough_draft.jpg)
## Companies model
I created a Django ORM that represented the company model from the image above. The model contained fields for name, industries, contact, size, status, amount donated, and date updated. I also registered this data model with Django's administrator so that models can be added and edited from the Django admin console.
## Companies view
I updated the Companies page I created for submission 1 to use Jinja templating to display the data from the companies table created from the model above. The companies are all rendered into a single table on the comapanies page.

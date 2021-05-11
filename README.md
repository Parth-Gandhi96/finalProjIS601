# IS 601 Web System Development
***
#### Final Project
**Devlopers** : 
- Aishwarya Allam *(aa362@njit.edu )*
- Parthkumar Anilkumar Gandhi *(pag36@njit.edu)*
****

#### Setup guide:
[Doc containing setup instruction step-by-step](Final%20Team%20Project%20Setup%20Guide%20-%20IS%20601.md)

#### Development Checklist:
*Parthkumar Anilkumar Gandhi*
- [X] Email to be sent to user for every following action: (SendGrid))
  - [X] Account verification after SignUp
  - [X] Once account is verified and user has successfully registered
  - [X] Forget password, to send reset URL
  - [X] After successfully changed the password
    
*Aishwarya Allam*  
- [X] Charts for following statistics: (plotly)
  - [X] Top 10 profitted
  - [X] IMDB wise Avg profit
  - [X] Genre wise Avg profit
  - [X] Last Five years Data
    
*Side features/task:*
- [X] Home page after signing in, explain about website and project
- [X] Logout option on Navbar
- [X] Create and write in README the GitHub pages URL


#### Running of the project:
[Doc with screenshots for explanation of running of the Project](Final%20Term%20Project%20Running%20-%20IS%20601.md)

#### Rest API GET requests:
*Backend by Parthkumar Anilkumar Gandhi*

| Request URL      | Description |
| :---        |    :----:   | 
| /top10ProfitedJSON   | JSON for Top 10 most profited movies from highest grossing movies DB  | 
| /avgProfitImdbWiseJSON      |  JSON for IMDB range wise Avg profit of movies from highest grossing movies DB       | 
| /avgProfitGenreWiseJSON   |  JSON for Genre wise Avg profit movies from highest grossing movies DB        | 
| /last5yearChartsJSON      |  JSON for movies released in last 5 year with box office and budget data from highest grossing movies DB       | 
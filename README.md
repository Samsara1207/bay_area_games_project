# bay_area_games_project
This project aims to address these core pain points by building an integrated digital solution, providing a modern, secure, and efficient platform for the management of the GBA Sports Games.

Django App 	Module	Database Table	Core Function
basic_info	Basic Information Module	team (representative team), athlete (athlete)	CRUD operations and eligibility verification for representative team and athlete information
event_management	Event Management Module	venue (venue), event (event), group (grouping), athlete_event (registration)	Venue management, event configuration, grouping, and athlete registration
referee_management	Referee and Result Module	referee (referee), referee_group (referee panel), referee_arrangement (referee assignment)	Referee management, paneling, and assignment scheduling
result_management	Result and Medal Module	result (result), medal_honor (medal & honor)	Result entry, ranking calculation, medal awarding, and record-breaking verification
logistics	Logistics Support Module	supplier (supplier), logistics_detail (support details), volunteer (volunteer)	Supplier management, logistics scheduling, and volunteer management
operation	Event Operation Module	schedule (schedule), event_operation (operation process)	Event schedule planning, operation process tracking, and exception handling
appeal_arbitration	Appeal and Arbitration Module	appeal (appeal), arbitration_committee (arbitration committee), appeal_arbitration (arbitration)	Appeal submission, arbitration handling, and result announcement
business	Commercial Operation Module	sponsor (sponsor), sponsor_rights (sponsorship rights), audience_ticket (ticketing)	Sponsor management, rights execution, and ticket sales
data_statistics	Data Statistics Module	data_report (statistics report)	Data statistics and report generation
 
<img width="864" height="606" alt="0a9e6435-4265-4913-9740-1c6543dbafcc" src="https://github.com/user-attachments/assets/085081df-8350-454a-8f73-ba158f903d8c" />
bay_area_games_project/
├── manage.py
├── bay_area_games/  # Project main directory (contains settings.py/urls.py/wsgi.py)
├── basic_info/      # Basic Information App
│   ├── models.py    # Models (Team/Athlete)
│   ├── serializers.py  # Serializers (data format conversion for API)
│   ├── views.py     # ViewSets (business logic processing)
│   ├── urls.py      # Sub URL routing (API path configuration)
│   ├── permissions.py  # Custom permissions (API access control)
│   └── filters.py   # Filters (data query condition filtering)
├── event_management/  # Event Management App (same structure as above)
├── referee_management/  # Referee Management App
├── result_management/  # Result and Medal Management App
├── logistics/  # Logistics Support App
├── operation/  # Event Operation App
├── appeal_arbitration/  # Appeal and Arbitration App
├── business/  # Commercial Operation App
├── finance_safety/  # Finance and Safety App
└── data_statistics/  # Data Statistics and Reporting App
 

 
Running Steps
Open Command Prompt (CMD) and navigate to the project directory.
Enter the command: cd [actual file path]
Input the command: python manage.py runserver
Open the project in your browser.
 
<img width="864" height="310" alt="image" src="https://github.com/user-attachments/assets/50db0c7f-7309-4c39-9835-b7f1a6600dfb" />


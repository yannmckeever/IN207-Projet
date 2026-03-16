# Location Management App

## Overview
The Location Management App is designed to facilitate the management of clients, rentals, rental options, and agencies within a rental service. This application provides a user-friendly interface for adding and managing these entities in a database.

## Features
- Add new clients to the database.
- Add new rentals to the database.
- Manage rental options.
- Add and manage agencies.

## Project Structure
```
location-management-app
├── src
│   ├── app.tsx                # Entry point of the application
│   ├── pages
│   │   └── Location
│   │       ├── index.tsx      # Main component for the Location page
│   │       ├── components
│   │       │   ├── ClientForm.tsx          # Form for adding clients
│   │       │   ├── RentalForm.tsx          # Form for adding rentals
│   │       │   ├── RentalOptionsForm.tsx   # Form for adding rental options
│   │       │   └── AgencyForm.tsx          # Form for adding agencies
│   │       └── types
│   │           └── index.ts    # TypeScript interfaces for data structures
│   ├── services
│   │   ├── clients.ts          # Functions for client database interactions
│   │   ├── rentals.ts          # Functions for rental database interactions
│   │   ├── rentalOptions.ts     # Functions for rental options management
│   │   └── agencies.ts         # Functions for agency management
│   └── types
│       └── index.ts            # Global TypeScript types
├── package.json                # npm configuration file
├── tsconfig.json               # TypeScript configuration file
└── README.md                   # Project documentation
```

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd location-management-app
   ```
3. Install the dependencies:
   ```
   npm install
   ```

## Usage
To start the application, run:
```
npm start
```
This will launch the application in your default web browser.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License.
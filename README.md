# Fleet Management System

This project is a comprehensive Java-based simulation of a vehicle fleet management system. It's designed to showcase core Object-Oriented Programming (OOP) principles through a practical application, featuring a detailed class hierarchy, a central management system, an interactive command-line interface (CLI), and data persistence functionality.

-----

## Demonstration of OOP Principles

This code serves as a practical example of the four major pillars of Object-Oriented Programming.

### 1\. Abstract Classes

Abstraction is used to model the concept of a `Vehicle` without needing to specify a concrete type.

  * The **`Vehicle`** class is `abstract`. It acts as a blueprint, declaring common properties (`id`, `model`) and abstract methods (`move`, `calculateFuelEfficiency`). It guarantees that any class extending `Vehicle` must provide its own implementation for these essential behaviors, but it cannot be instantiated itself.
  * Intermediate classes like **`LandVehicle`**, **`AirVehicle`**, and **`WaterVehicle`** are also abstract. They provide another layer of abstraction, adding properties relevant to their domain (e.g., `numWheels` for `LandVehicle`) and providing specialized implementations for methods like `estimateJourneyTime`.

### 2\. Inheritance

Inheritance is used to create a logical "is-a" relationship between vehicle types, promoting code reuse.

  * A **`Car`** *is-a* **`LandVehicle`**, which in turn *is-a* **`Vehicle`**.
  * This structure allows the `Car` class to inherit properties and methods from both `LandVehicle` (like `getNumWheels()`) and `Vehicle` (like `getId()` and `getModel()`), avoiding redundant code.

### 3\. Polymorphism

Polymorphism (meaning "many forms") allows objects of different classes to be treated as objects of a common superclass. This is most evident in the `FleetManager`.

  * The `FleetManager` holds a `List<Vehicle>`, which can contain `Car`, `Truck`, `Airplane`, and `CargoShip` objects simultaneously.
  * When `fleetManager.startAllJourneys(distance)` is called, it iterates through the list and calls `v.move(distance)` on each object.
  * The Java Virtual Machine (JVM) determines at runtime which specific `move()` method to execute—the one defined in `Car`, `Airplane`, etc. This is **runtime polymorphism**. The same method call (`v.move()`) results in different behavior depending on the object's actual type.

### 4\. Interfaces

Interfaces are used to define common capabilities or contracts that classes can implement, independent of their position in the class hierarchy. This allows for great flexibility.

  * Interfaces like **`FuelConsumable`**, **`CargoCarrier`**, and **`PassengerCarrier`** define what a vehicle *can do*.
  * For example, both a `Bus` (a `LandVehicle`) and an `Airplane` (an `AirVehicle`) can carry cargo, so they both implement the `CargoCarrier` interface. This is more flexible than trying to build this functionality into the `Vehicle` class hierarchy.
  * This allows the `FleetManager` to interact with vehicles based on their capabilities, such as performing maintenance only on objects that are an `instanceof` the `Maintainable` interface.

-----

## Project Structure

The project is organized into distinct packages, each with a specific responsibility. 📂

```
/
├── Abstract_Classes/
│   ├── Vehicle.java
│   ├── AirVehicle.java
│   ├── LandVehicle.java
│   └── WaterVehicle.java
│
├── Concrete_Classes/
│   ├── Airplane.java
│   ├── Bus.java
│   ├── Car.java
│   ├── CargoShip.java
│   └── Truck.java
│
├── Exceptions/
│   ├── InsufficientFuelException.java
│   ├── InvalidOperationException.java
│   └── OverloadException.java
│
├── Fleet_Manager/
│   └── FleetManager.java
│
├── Interfaces/
│   ├── CargoCarrier.java
│   ├── FuelConsumable.java
│   ├── Maintainable.java
│   └── PassengerCarrier.java
│
├── Main/
│   └── Main.java
│
└── Persistence/
    ├── FleetLoader.java
    └── savetoCSV.java
```

### Folder and File Explanations

  * **`Abstract_Classes/`**: Contains the abstract base classes that form the foundation of the vehicle hierarchy.

      * `Vehicle.java`: The ultimate base class for all vehicles, defining common properties and abstract methods.
      * `AirVehicle.java`: Extends `Vehicle` for flying vehicles, adding properties like `maxAltitude`.
      * `LandVehicle.java`: Extends `Vehicle` for ground vehicles, adding `numWheels`.
      * `WaterVehicle.java`: Extends `Vehicle` for watercraft, adding properties like `hasSail`.

  * **`Concrete_Classes/`**: Contains the specific, instantiable implementations of the abstract vehicle classes.

      * `Airplane.java`: A concrete `AirVehicle` that can carry passengers and cargo.
      * `Bus.java`: A concrete `LandVehicle` for carrying both passengers and cargo.
      * `Car.java`: A concrete `LandVehicle` primarily for carrying passengers.
      * `CargoShip.java`: A concrete `WaterVehicle` for transporting cargo.
      * `Truck.java`: A concrete `LandVehicle` designed for heavy cargo transport.

  * **`Exceptions/`**: Holds custom exception classes used for specific error handling scenarios.

      * `InsufficientFuelException.java`: Thrown when a vehicle does not have enough fuel for a journey.
      * `InvalidOperationException.java`: Used for general operational errors like invalid input or duplicate IDs.
      * `OverloadException.java`: Thrown when a vehicle's cargo or passenger capacity is exceeded.

  * **`Fleet_Manager/`**: Contains the central logic for managing the collection of vehicles.

      * `FleetManager.java`: The core class that adds, removes, and operates on the list of vehicles, and generates reports.

  * **`Interfaces/`**: Defines contracts for behaviors that can be implemented by any vehicle class, regardless of its inheritance.

      * `CargoCarrier.java`: Defines methods for loading and unloading cargo.
      * `FuelConsumable.java`: Defines methods for refueling and consuming fuel.
      * `Maintainable.java`: Defines methods related to vehicle maintenance.
      * `PassengerCarrier.java`: Defines methods for boarding and disembarking passengers.

  * **`Main/`**: Contains the application's entry point.

      * `Main.java`: Contains the `main` method which runs the command-line interface (CLI) for user interaction.

  * **`Persistence/`**: Handles saving and loading the fleet data to and from files.

      * `FleetLoader.java`: Reads a CSV file to reconstruct and load vehicle objects into the fleet.
      * `savetoCSV.java`: Saves the current state of the fleet into a CSV file.

-----

## Getting Started

Follow these instructions to compile and run the application.

### Prerequisites

  * Java Development Kit (JDK) 8 or higher.

### Compilation

1.  Place all the provided `.java` files into their respective package directories as shown in the structure above.
2.  Navigate to the root directory that contains the `Main`, `Persistence`, `Fleet_Manager`, etc., folders.
3.  Compile all Java source files using the following command:
    ```bash
    javac */*.java
    ```

### Running the Application

Execute the `main` method from the `Main` class using its fully qualified name:

```bash
java Main.Main
```

This will launch the interactive command-line interface.

-----

## Using the Command-Line Interface (CLI)

The application provides a menu-driven CLI to interact with the fleet.

  * **1. Add Vehicle**: Prompts you to choose a vehicle type and enter its details to add it to the fleet.
  * **2. Remove Vehicle**: Deletes a vehicle from the fleet using its unique ID.
  * **3. Start Journey**: Simulates all vehicles traveling a specified distance, checking for sufficient fuel.
  * **4. Refuel All**: Adds a specified amount of fuel to all `FuelConsumable` vehicles.
  * **5. Perform Maintenance**: Performs maintenance on all vehicles that need it.
  * **6. Generate Report**: Displays a summary of the fleet, including vehicle counts by type, total mileage, and maintenance needs.
  * **7. Save Fleet**: Saves the current state of all vehicles in the fleet to a `.csv` file.
  * **8. Load Fleet**: Loads a fleet of vehicles from a `.csv` file, with an option to append or replace the current fleet.
  * **9. Search by Type**: Lists all vehicles of a specific type.
  * **10. List Vehicles Needing Maintenance**: Shows only the vehicles that require maintenance.
  * **11. Exit**: Closes the application.

-----

## Persistence: Saving and Loading the Fleet

The application can save and load the fleet's state, allowing data to persist between sessions. 💾

  * **Saving**: The "Save Fleet" option uses the `savetoCSV` class to write each vehicle's data to a new line in the specified file. The data is stored in a `key:value` format, separated by commas (e.g., `Class:Car,ID:C-001,Model:Civic,...`).
  * **Loading**: The "Load Fleet" option uses the `FleetLoader` class to read a file with the same format. It parses each line, reconstructs the appropriate vehicle object, and adds it to the fleet in memory.

-----

## Demo Walkthrough

Here is a sample session demonstrating the application's core features. 🚀

### Step 1: Start the application

```bash
java Main.Main
```

**Expected Output:**

```
=== Fleet Management System ===
1. Add Vehicle
2. Remove Vehicle
...
11. Exit
Enter choice:
```

### Step 2: Add a Car and an Airplane

  * Choose option `1`. Enter `Car` and provide details when prompted.
  * Choose option `1` again. Enter `Airplane` and provide its details.

**Expected Output (after each addition):**

```
Vehicle with ID ... added to fleet
```

### Step 3: Generate a Report

  * Choose option `6`.

**Expected Output:**

```
==== Fleet Report ====
Total vehicles: 2
Vehicle count by type:
 - Car: 1
 - Airplane: 1
Average fuel efficiency: ...
Total mileage: ...
Vehicles needing maintenance: ...
====================
```

### Step 4: Simulate a Journey

  * Choose option `3` and enter distance `100`.

**Expected Output:**

```
Driving on road.....
Vehicle C-001 completed journey of 100.0 km.
“Flying at height of ... meters........
Vehicle A-747 completed journey of 100.0 km.
```

### Step 5: Save the Fleet

  * Choose option `7` and enter filename `my_fleet.csv`.

**Expected Output:**

```
Fleet saved to my_fleet.csv
```

You can now open `my_fleet.csv` and see the saved data.

### Step 6: Clear and Load the Fleet

  * To test loading, first remove a vehicle. Choose option `2` and enter its ID.
  * Now, choose option `8` to load the fleet.
      * Enter filename `my_fleet.csv`.
      * Choose to replace the existing fleet.

**Expected Output:**

```
Vehicle ... removed successfully.
...
Replacing existing fleet...
Fleet loaded from my_fleet.csv
Fleet loaded successfully!
```

### Step 7: Verify the Fleet was Restored

  * Choose option `6` to generate a report again. The report should be identical to the one from Step 3, showing the vehicles have been successfully restored from the file.

### Step 8: Exit

  * Choose option `11`.

**Expected Output:**

```
Exiting... Goodbye!
```

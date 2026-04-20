/*
 * =============================================
 *   STUDENT ADMISSION MANAGEMENT SYSTEM
 * =============================================
 *  Two users: Admin and Student
 *  Data saved to file (students.txt)
 * =============================================
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// ─────────────────────────────────────────
//  STRUCT - One student = one node
// ─────────────────────────────────────────
struct Student {
    int id;                  // auto assigned internally
    char name[50];
    char phone[15];
    char email[50];
    float marks;
    char desiredBranch[30];

    // Assigned by admin AFTER approval
    int rollNo;              // 0 means not assigned yet
    char assignedBranch[30]; // empty means not assigned yet

    char status[15];         // "Pending" / "Approved" / "Rejected"

    struct Student* next;
};

// ─────────────────────────────────────────
//  GLOBAL HEAD + ID COUNTER
// ─────────────────────────────────────────
struct Student* head = NULL;
int nextId = 1;  // auto increment id for each student

// ─────────────────────────────────────────
//  HELPER - clear screen & pause
// ─────────────────────────────────────────
void clearScreen() {
    #ifdef _WIN32
        system("cls");
    #else
        system("clear");
    #endif
}

void pause() {
    printf("\nPress Enter to continue...");
    getchar();
    getchar();
}

// ─────────────────────────────────────────
//  FILE - Save all students to file
// ─────────────────────────────────────────
void saveToFile() {
    FILE* file = fopen("students.txt", "w");
    if (file == NULL) {
        printf("Error: Could not save data!\n");
        return;
    }

    // First line = nextId so we remember the counter
    fprintf(file, "%d\n", nextId);

    struct Student* temp = head;
    while (temp != NULL) {
        fprintf(file, "%d|%s|%s|%s|%.2f|%s|%d|%s|%s\n",
            temp->id,
            temp->name,
            temp->phone,
            temp->email,
            temp->marks,
            temp->desiredBranch,
            temp->rollNo,
            temp->assignedBranch,
            temp->status
        );
        temp = temp->next;
    }

    fclose(file);
}

// ─────────────────────────────────────────
//  FILE - Load all students from file
// ─────────────────────────────────────────
void loadFromFile() {
    FILE* file = fopen("students.txt", "r");
    if (file == NULL) {
        // No file yet, that's fine
        return;
    }

    // Read the id counter first
    fscanf(file, "%d\n", &nextId);

    char line[300];
    while (fgets(line, sizeof(line), file)) {
        struct Student* newStudent = (struct Student*)malloc(sizeof(struct Student));

        // Parse the line using | as separator
        char* token;

        token = strtok(line, "|"); newStudent->id          = atoi(token);
        token = strtok(NULL, "|"); strcpy(newStudent->name,          token);
        token = strtok(NULL, "|"); strcpy(newStudent->phone,         token);
        token = strtok(NULL, "|"); strcpy(newStudent->email,         token);
        token = strtok(NULL, "|"); newStudent->marks        = atof(token);
        token = strtok(NULL, "|"); strcpy(newStudent->desiredBranch, token);
        token = strtok(NULL, "|"); newStudent->rollNo       = atoi(token);
        token = strtok(NULL, "|"); strcpy(newStudent->assignedBranch,token);
        token = strtok(NULL, "\n"); strcpy(newStudent->status,       token);

        newStudent->next = NULL;

        // Add to end of linked list
        if (head == NULL) {
            head = newStudent;
        } else {
            struct Student* temp = head;
            while (temp->next != NULL) temp = temp->next;
            temp->next = newStudent;
        }
    }

    fclose(file);
}

// ─────────────────────────────────────────
//  LINKED LIST - Add new student at end
// ─────────────────────────────────────────
void addStudent(char name[], char phone[], char email[], float marks, char desiredBranch[]) {
    struct Student* newStudent = (struct Student*)malloc(sizeof(struct Student));

    newStudent->id     = nextId++;
    strcpy(newStudent->name,          name);
    strcpy(newStudent->phone,         phone);
    strcpy(newStudent->email,         email);
    newStudent->marks  = marks;
    strcpy(newStudent->desiredBranch, desiredBranch);

    // Not assigned yet
    newStudent->rollNo = 0;
    strcpy(newStudent->assignedBranch, "N/A");
    strcpy(newStudent->status, "Pending");

    newStudent->next = NULL;

    if (head == NULL) {
        head = newStudent;
    } else {
        struct Student* temp = head;
        while (temp->next != NULL) temp = temp->next;
        temp->next = newStudent;
    }

    saveToFile();
    printf("\n Application submitted! Your Application ID is: %d\n", newStudent->id);
    printf(" Keep this ID to check your status later.\n");
}

// ─────────────────────────────────────────
//  LINKED LIST - Find student by ID
// ─────────────────────────────────────────
struct Student* findById(int id) {
    struct Student* temp = head;
    while (temp != NULL) {
        if (temp->id == id) return temp;
        temp = temp->next;
    }
    return NULL;
}

// ─────────────────────────────────────────
//  LINKED LIST - Find student by phone
// ─────────────────────────────────────────
struct Student* findByPhone(char phone[]) {
    struct Student* temp = head;
    while (temp != NULL) {
        if (strcmp(temp->phone, phone) == 0) return temp;
        temp = temp->next;
    }
    return NULL;
}

// ─────────────────────────────────────────
//  LINKED LIST - Delete student by ID
// ─────────────────────────────────────────
void deleteStudent(int id) {
    if (head == NULL) {
        printf(" No records found.\n");
        return;
    }

    // If head itself is the one to delete
    if (head->id == id) {
        struct Student* temp = head;
        head = head->next;
        free(temp);
        saveToFile();
        printf(" Student record deleted.\n");
        return;
    }

    // Find the node before target
    struct Student* prev = head;
    while (prev->next != NULL && prev->next->id != id) {
        prev = prev->next;
    }

    if (prev->next == NULL) {
        printf(" Student with ID %d not found.\n", id);
        return;
    }

    struct Student* temp = prev->next;
    prev->next = temp->next;
    free(temp);
    saveToFile();
    printf(" Student record deleted.\n");
}

// ─────────────────────────────────────────
//  DISPLAY - Print one student row
// ─────────────────────────────────────────
void printStudentRow(struct Student* s) {
    printf("\n ─────────────────────────────────────────\n");
    printf("  Application ID : %d\n",   s->id);
    printf("  Name           : %s\n",   s->name);
    printf("  Phone          : %s\n",   s->phone);
    printf("  Email          : %s\n",   s->email);
    printf("  Marks          : %.2f%%\n", s->marks);
    printf("  Desired Branch : %s\n",   s->desiredBranch);
    printf("  Status         : %s\n",   s->status);
    if (strcmp(s->status, "Approved") == 0) {
        printf("  Roll No        : %d\n",   s->rollNo);
        printf("  Assigned Branch: %s\n",   s->assignedBranch);
    }
    printf(" ─────────────────────────────────────────\n");
}

// ─────────────────────────────────────────
//  DISPLAY - Print all students
// ─────────────────────────────────────────
void displayAll() {
    if (head == NULL) {
        printf("\n No applications found.\n");
        return;
    }
    struct Student* temp = head;
    int count = 0;
    while (temp != NULL) {
        printStudentRow(temp);
        count++;
        temp = temp->next;
    }
    printf("\n Total Applications: %d\n", count);
}

// ─────────────────────────────────────────
//  ADMIN - Approve a student
// ─────────────────────────────────────────
void approveStudent() {
    int id, rollNo;
    char branch[30];

    printf("\n Enter Application ID to approve: ");
    scanf("%d", &id);

    struct Student* s = findById(id);
    if (s == NULL) {
        printf(" Student not found!\n");
        return;
    }
    if (strcmp(s->status, "Approved") == 0) {
        printf(" Already approved!\n");
        return;
    }

    printStudentRow(s);

    printf(" Assign Roll No : ");
    scanf("%d", &rollNo);
    printf(" Assign Branch  : ");
    scanf("%s", branch);

    s->rollNo = rollNo;
    strcpy(s->assignedBranch, branch);
    strcpy(s->status, "Approved");

    saveToFile();
    printf("\n Student APPROVED successfully!\n");
}

// ─────────────────────────────────────────
//  ADMIN - Reject a student
// ─────────────────────────────────────────
void rejectStudent() {
    int id;
    printf("\n Enter Application ID to reject: ");
    scanf("%d", &id);

    struct Student* s = findById(id);
    if (s == NULL) {
        printf(" Student not found!\n");
        return;
    }

    strcpy(s->status, "Rejected");
    saveToFile();
    printf("\n Student application REJECTED.\n");
}

// ─────────────────────────────────────────
//  ADMIN - Search by name
// ─────────────────────────────────────────
void searchByName() {
    char name[50];
    printf("\n Enter name to search: ");
    scanf(" %[^\n]", name);

    struct Student* temp = head;
    int found = 0;
    while (temp != NULL) {
        // Check if name contains the search string
        if (strstr(temp->name, name) != NULL) {
            printStudentRow(temp);
            found++;
        }
        temp = temp->next;
    }
    if (!found) printf(" No student found with that name.\n");
}

// ─────────────────────────────────────────
//  ADMIN MENU
// ─────────────────────────────────────────
void adminMenu() {
    char password[20];
    printf("\n Enter Admin Password: ");
    scanf("%s", password);

    // Simple hardcoded password
    if (strcmp(password, "admin123") != 0) {
        printf(" Wrong password!\n");
        return;
    }

    int choice;
    do {
        clearScreen();
        printf("\n ╔══════════════════════════════╗");
        printf("\n ║       ADMIN DASHBOARD        ║");
        printf("\n ╠══════════════════════════════╣");
        printf("\n ║  1. View All Applications    ║");
        printf("\n ║  2. Approve Student          ║");
        printf("\n ║  3. Reject Student           ║");
        printf("\n ║  4. Delete a Record          ║");
        printf("\n ║  5. Search by Name           ║");
        printf("\n ║  0. Logout                   ║");
        printf("\n ╚══════════════════════════════╝");
        printf("\n Enter choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1: displayAll();    pause(); break;
            case 2: approveStudent(); pause(); break;
            case 3: rejectStudent(); pause(); break;
            case 4: {
                int id;
                printf("\n Enter Application ID to delete: ");
                scanf("%d", &id);
                deleteStudent(id);
                pause();
                break;
            }
            case 5: searchByName(); pause(); break;
            case 0: printf("\n Logged out.\n"); break;
            default: printf("\n Invalid choice!\n"); pause();
        }
    } while (choice != 0);
}

// ─────────────────────────────────────────
//  STUDENT - Fill application form
// ─────────────────────────────────────────
void studentApply() {
    char name[50], phone[15], email[50], branch[30];
    float marks;

    printf("\n ── Fill Your Application Form ──\n");
    printf(" Name          : ");
    scanf(" %[^\n]", name);
    printf(" Phone Number  : ");
    scanf("%s", phone);

    // Check if phone already registered
    if (findByPhone(phone) != NULL) {
        printf("\n This phone number is already registered!\n");
        printf(" Use 'Check Status' option to see your application.\n");
        return;
    }

    printf(" Email         : ");
    scanf("%s", email);
    printf(" Marks (%%)     : ");
    scanf("%f", &marks);
    printf(" Desired Branch: ");
    scanf("%s", branch);

    addStudent(name, phone, email, marks, branch);
}

// ─────────────────────────────────────────
//  STUDENT - Check their own status
// ─────────────────────────────────────────
void checkStatus() {
    int choice;
    printf("\n Search by:\n");
    printf(" 1. Application ID\n");
    printf(" 2. Phone Number\n");
    printf(" Enter choice: ");
    scanf("%d", &choice);

    if (choice == 1) {
        int id;
        printf(" Enter your Application ID: ");
        scanf("%d", &id);
        struct Student* s = findById(id);
        if (s == NULL) printf(" No application found!\n");
        else printStudentRow(s);

    } else if (choice == 2) {
        char phone[15];
        printf(" Enter your Phone Number: ");
        scanf("%s", phone);
        struct Student* s = findByPhone(phone);
        if (s == NULL) printf(" No application found!\n");
        else printStudentRow(s);

    } else {
        printf(" Invalid choice!\n");
    }
}

// ─────────────────────────────────────────
//  STUDENT MENU
// ─────────────────────────────────────────
void studentMenu() {
    int choice;
    do {
        clearScreen();
        printf("\n ╔══════════════════════════════╗");
        printf("\n ║       STUDENT PORTAL         ║");
        printf("\n ╠══════════════════════════════╣");
        printf("\n ║  1. Apply for Admission      ║");
        printf("\n ║  2. Check My Status          ║");
        printf("\n ║  0. Back                     ║");
        printf("\n ╚══════════════════════════════╝");
        printf("\n Enter choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1: studentApply(); pause(); break;
            case 2: checkStatus();  pause(); break;
            case 0: break;
            default: printf("\n Invalid choice!\n"); pause();
        }
    } while (choice != 0);
}

// ─────────────────────────────────────────
//  MAIN MENU
// ─────────────────────────────────────────
int main() {
    loadFromFile();  // Load saved data when program starts

    int choice;
    do {
        clearScreen();
        printf("\n ╔══════════════════════════════╗");
        printf("\n ║  STUDENT ADMISSION SYSTEM    ║");
        printf("\n ╠══════════════════════════════╣");
        printf("\n ║  1. Admin Login              ║");
        printf("\n ║  2. Student Portal           ║");
        printf("\n ║  0. Exit                     ║");
        printf("\n ╚══════════════════════════════╝");
        printf("\n Enter choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1: adminMenu();   break;
            case 2: studentMenu(); break;
            case 0: printf("\n Goodbye!\n\n"); break;
            default: printf("\n Invalid choice!\n"); pause();
        }
    } while (choice != 0);

    return 0;
}

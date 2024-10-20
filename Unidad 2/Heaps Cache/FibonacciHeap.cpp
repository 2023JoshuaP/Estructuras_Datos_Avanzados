#include<bits/stdc++.h>
#include<conio.h>
using namespace std; 

#define NINF INT_MIN
// Creating a structure to represent a node in the heap 
struct node 
{ 
	node* parent; // Parent pointer 
	node* child; // Child pointer 
	node* left; // Pointer to the node on the left 
	node* right; // Pointer to the node on the right 
	int key; // Value of the node 
	int degree; // Degree of the node 
	char mark; // Black or white mark of the node 
	char c; // Flag for assisting in the Find node function 
}; 

// Creating min pointer as "mini" 
struct node* mini = NULL; 

// Declare an integer for number of nodes in the heap 
int no_of_nodes = 0; 

// Function to insert a node in heap 
void insertion(int val) 
{ 
	struct node* new_node = (struct node*)malloc(sizeof(struct node)); 
	new_node->key = val; 
	new_node->degree = 0; 
	new_node->mark = 'W'; 
	new_node->c = 'N'; 
	new_node->parent = NULL; 
	new_node->child = NULL; 
	new_node->left = new_node; 
	new_node->right = new_node; 
	if (mini != NULL) { 
		(mini->left)->right = new_node; 
		new_node->right = mini; 
		new_node->left = mini->left; 
		mini->left = new_node; 
		if (new_node->key < mini->key) 
			mini = new_node; 
	} 
	else { 
		mini = new_node; 
	} 
	no_of_nodes++; 
} 
// Linking the heap nodes in parent child relationship 
void Fibonnaci_link(struct node* ptr2, struct node* ptr1) 
{ 
	(ptr2->left)->right = ptr2->right; 
	(ptr2->right)->left = ptr2->left; 
	if (ptr1->right == ptr1) 
		mini = ptr1; 
	ptr2->left = ptr2; 
	ptr2->right = ptr2; 
	ptr2->parent = ptr1; 
	if (ptr1->child == NULL) 
		ptr1->child = ptr2; 
	ptr2->right = ptr1->child; 
	ptr2->left = (ptr1->child)->left; 
	((ptr1->child)->left)->right = ptr2; 
	(ptr1->child)->left = ptr2; 
	if (ptr2->key < (ptr1->child)->key) 
		ptr1->child = ptr2; 
	ptr1->degree++; 
} 
// Consolidating the heap 
void Consolidate() 
{ 
	int temp1; 
	float temp2 = (log(no_of_nodes)) / (log(2)); 
	int temp3 = temp2; 
	struct node* arr[temp3]; 
	for (int i = 0; i <= temp3; i++) 
		arr[i] = NULL; 
	node* ptr1 = mini; 
	node* ptr2; 
	node* ptr3; 
	node* ptr4 = ptr1; 
	do { 
		ptr4 = ptr4->right; 
		temp1 = ptr1->degree; 
		while (arr[temp1] != NULL) { 
			ptr2 = arr[temp1]; 
			if (ptr1->key > ptr2->key) { 
				ptr3 = ptr1; 
				ptr1 = ptr2; 
				ptr2 = ptr3; 
			} 
			if (ptr2 == mini) 
				mini = ptr1; 
			Fibonnaci_link(ptr2, ptr1); 
			if (ptr1->right == ptr1) 
				mini = ptr1; 
			arr[temp1] = NULL; 
			temp1++; 
		} 
		arr[temp1] = ptr1; 
		ptr1 = ptr1->right; 
	} while (ptr1 != mini); 
	mini = NULL; 
	for (int j = 0; j <= temp3; j++) { 
		if (arr[j] != NULL) { 
			arr[j]->left = arr[j]; 
			arr[j]->right = arr[j]; 
			if (mini != NULL) { 
				(mini->left)->right = arr[j]; 
				arr[j]->right = mini; 
				arr[j]->left = mini->left; 
				mini->left = arr[j]; 
				if (arr[j]->key < mini->key) 
					mini = arr[j]; 
			} 
			else { 
				mini = arr[j]; 
			} 
			if (mini == NULL) 
				mini = arr[j]; 
			else if (arr[j]->key < mini->key) 
				mini = arr[j]; 
		} 
	} 
} 

// Function to extract minimum node in the heap 
void Extract_min() 
{ 
	if (mini == NULL) 
		cout << "The heap is empty!!" << endl; 
	else { 
		node* temp = mini; 
		node* pntr; 
		pntr = temp; 
		node* x = NULL; 
		if (temp->child != NULL) { 

			x = temp->child; 
			do { 
				pntr = x->right; 
				(mini->left)->right = x; 
				x->right = mini; 
				x->left = mini->left; 
				mini->left = x; 
				if (x->key < mini->key) 
					mini = x; 
				x->parent = NULL; 
				x = pntr; 
			} while (pntr != temp->child); 
		} 
		(temp->left)->right = temp->right; 
		(temp->right)->left = temp->left; 
		mini = temp->right; 
		if (temp == temp->right && temp->child == NULL) 
			mini = NULL; 
		else { 
			mini = temp->right; 
			Consolidate(); 
		} 
		no_of_nodes--; 
	} 
} 

// Cutting a node in the heap to be placed in the root list 
void Cut(struct node* found, struct node* temp) 
{ 
	if (found == found->right) 
		temp->child = NULL; 

	(found->left)->right = found->right; 
	(found->right)->left = found->left; 
	if (found == temp->child) 
		temp->child = found->right; 

	temp->degree = temp->degree - 1; 
	found->right = found; 
	found->left = found; 
	(mini->left)->right = found; 
	found->right = mini; 
	found->left = mini->left; 
	mini->left = found; 
	found->parent = NULL; 
	found->mark = 'B'; 
} 

// Recursive cascade cutting function 
void Cascase_cut(struct node* temp) 
{ 
	node* ptr5 = temp->parent; 
	if (ptr5 != NULL) { 
		if (temp->mark == 'W') { 
			temp->mark = 'B'; 
		} 
		else { 
			Cut(temp, ptr5); 
			Cascase_cut(ptr5); 
		} 
	} 
} 
// Function to find the given node 
node* Find(struct node* mini, int val) 
{ 
	if(mini == NULL)
	{
		return NULL;
	}
	struct node* found = mini; 
	node* temp5 = mini; 
	temp5->c = 'Y'; 
	node* found_ptr = NULL; 
	if (temp5->key == val) 
	{ 
		found_ptr = temp5; 
		temp5->c = 'N'; 
		found = found_ptr; 
		return found; 
	} 
	if (found_ptr == NULL) 
	{ 
		if (temp5->child != NULL) 
			found_ptr = Find(temp5->child, val); 
		if ((temp5->right)->c != 'Y') 
			found_ptr = Find(temp5->right,val); 
	} 
	temp5->c = 'N'; 
	found = found_ptr; 
	return found;
} 

// Function to decrease the value of a node in the heap 
void Decrease_key(struct node* mini, int old_val, int val) 
{ 
	if (mini == NULL) 
	{
		cout << "The Heap is Empty!!" << endl;
		return; 
	}
	node *found = Find(mini, old_val);
	if(found == NULL)
	{
		cout << "Node not found in the Heap!!" << endl;
		return; 
	}

	if(old_val < val)
	{
		cout << "Entered key greater than current key!!" << endl;
		return;
	}

	found->key = val;

	struct node* temp = found->parent; 
	if (temp != NULL && found->key < temp->key) { 
		Cut(found, temp); 
		Cascase_cut(temp); 
	} 
	if (found->key < mini->key) 
	{
		::mini = found; 
	}
} 

// Deleting a node from the heap 
void Deletion(int val) 
{ 
	if (mini == NULL) 
		cout << "The heap is empty!!" << endl; 
	else { 

		node *found = Find(mini, val);
		if(found == NULL)
		{
			cout << "The key is not present!" << endl;
			return;
		}
		// Decreasing the value of the node to -infinty
		Decrease_key(mini, val, NINF); 

		// Calling Extract_min function to 
		// delete minimum value node, which is -infnity 

		Extract_min(); 
		cout << "Key Deleted!" << endl; 
	} 
} 

// Function to display the heap 
void display() 
{ 
	node* ptr = mini; 
	if (ptr == NULL) 
		cout << "The Heap is Empty!!" << endl; 

	else 
	{ 
		cout << "The root node(s) of Heap are: " << endl; 
		do 
		{ 
			cout << ptr->key; 
			ptr = ptr->right; 
			if (ptr != mini) 
			{ 
				cout << "-->"; 
			} 
		} while (ptr != mini && ptr->right != NULL); 
		cout << endl << "The heap has " << no_of_nodes << " nodes" << endl << endl; 
	} 
} 

// Driver code 
int main() 
{ 
	while(1)
	{
		cout << "---------------------------------" << endl;
		cout << "\tFibonacci Heap" << endl;
		cout << "---------------------------------" << endl;
		cout << "Menu:" << endl;
		cout << "1. Insertion of keys\n2. Extract Minimum\n3. Decrease Key\n4. Deletion of Keys\n5. Searching\n6. Display Root Node(s)\n7. Exit" << endl;
		int choice;
		cout << "Choose the operation: ";
		cin >> choice;
		cout << "---------------------------------" << endl;
		switch(choice)
		{
			case 1: 
			{
				cout << "Enter the no. of Keys you want to insert in the heap: ";
				int n;
				cin >> n;
				for(int i = 0; i < n; i++)
				{
					int key;
					cout << "Enter the key " << i + 1 << ": ";
					cin >> key;
					insertion(key);
				}
			}
			break;
			case 2:
			{
				cout << "Extracting Minimum" << endl;
				Extract_min();
			}
			break;
			case 3:
			{
				int key;
				cout << "Enter the key you want to decrease: ";
				cin >> key;
				int new_val;
				cout << "Decrease value to: ";
				cin >> new_val;
				Decrease_key(mini, key, new_val);
			}
			break;
			case 4:
			{
				cout << "Enter the no. of Keys you want to delete from the heap: ";
				int n;
				cin >> n;
				for(int i = 0; i < n; i++)
				{
					int key;
					cout << "Enter the key " << i + 1 << ": ";
					cin >> key;
					Deletion(key);
				}
			}
			break;
			case 5:
			{
				int key;
				cout << "Enter key to be searched: ";
				cin >> key;
				if(mini == NULL)
				{
					cout << "Heap is Empty!" << endl;
					break;
				}
				node *found = Find(mini, key);
				if(found == NULL)
				{
					cout << "The key is not present!" << endl;
				}
				else
				{
					cout << "The key is present!" << endl;
				}
			}
			break;
			case 6:
			{
				display();
			}
			break;
			case 7:
			{
				cout << "Quitting... Press any key!" << endl;
				getch();
				exit(1);
			}
		}
	}
	return 0; 
} 
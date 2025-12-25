import sqlite3 as sq

# BUSINESS PROFILE MANAGER
class BusinessProfileManager:
    def __init__(self):
        self.conn = sq.connect("business.db")
        self.cur = self.conn.cursor()
        self.create_table()
        
        
    def create_table(self):
        # self.cur.execute("DROP TABLE IF EXISTS clients")
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS clients (id INTEGER PRIMARY KEY AUTOINCREMENT, fullname TEXT, product TEXT, price REAL)"
        )
        self.conn.commit()
        
        
    def add_client(self):
        while True:
            fullname = input("Enter fullname: ").strip()
           
            if not fullname:
                print("Update cancelled")
                return
           
            product = input("Input your product: ").strip()
           
            if not product:
                print("Update cancelled")
                return
           
            try:
                price = float(input("Price for product: "))
                self.cur.execute(
                    "INSERT INTO clients (fullname, product, price) VALUES (?, ?, ?)",
                    (fullname, product, price)
                )
                self.conn.commit()
          
            except ValueError:
                print("Invalid input! Numbers only!")
                return
           
            if self.cur.rowcount > 0:
                print("Update successful")
                break
            
   
    def show_clients(self):
        self.cur.execute("SELECT id, fullname, product, price FROM clients")
        rows = self.cur.fetchall()
        
        if not rows:
            print("No added yet!")
       
        else:
            print("📋 LIST OF MY PERSONAL CLIENTS:")
            print("─" * 50)
            
            for row in rows:
                print(f"🆔 ID       : {row[0]}")
                print(f"👤 Fullname : {row[1]:<20}")
                print(f"📦 Product  : {row[2]:<15}")
                print(f"💰 Price    : ₱{row[3]:>10,.2f}")
                print("─" * 50)
                    
        
    def delete_client(self):
        while True:
            try:
                client_id = int(input("🗑️ Enter Profile ID to delete: "))
                self.cur.execute("DELETE FROM clients WHERE id=?", (client_id,))
                self.conn.commit()
                
            except ValueError:
                print("Invalid input! Numbers only!")
                return 
            
            if self.cur.rowcount == 0:
                print(f"({client_id}) Delete failed!")
                return
           
            else:
                print(f"({client_id}) Delete Successful.")
                return
            
            
    def update_client(self):
        while True:
            try:
                client_id = int(input("📝 Enter the ID to update: "))
                   
            except ValueError:             
                print("⚠️ Only numbers allowed. Try again.")
                return
                      
            fullname = input("📝 Input new full name: ").strip()
         
            if not fullname:
                print("Update cancelled")
                return
           
            product = input("📦 Input new product: ").strip()
             
            if not product:
                print("Update cancelled")
                return
            
            try:
                price = float(input("💰 Input new price: "))
                
                if not price:
                    print("Update cancelled!")
                    return
                
            except ValueError:
                print("Invalid input! Numbers only!")
                return
        
            self.cur.execute(
                "UPDATE clients SET fullname=?, product=?, price=? WHERE id=?",
                (fullname, product, price, client_id)
            )
            self.conn.commit()
            
            if self.cur.rowcount > 0:
                print("Update successful.")
                return
            
               
    def advanced_search(self):
        
        def search_by_id():
            while True:
                try:
                    client_id = int(input("Select ID you want to see: "))
             
            
                except ValueError:
                    print("❌ Invalid input! Please enter a number.")
                    return
             
                self.cur.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
                row = self.cur.fetchone()
              
                if row:
                    print(f"✅ Selection successful → {row}")
                else:
                    print("❌ Selection failed → ID not found")
              
                again = input("Again? (yes/no): ").strip().lower()
                if again != "yes":
                    print("🔥 Thanks for using!")
                    break
              
              
        def search_with_and():
            while True:
                fullname = input("Enter fullname: ").strip()
              
                if not fullname:
                    print("❌ Program cancelled!")
                    return
             
                product = input("Enter product: ").strip()
                    
                if not product:
                    print("❌ Program cancelled!")
                    return
             
                self.cur.execute(
                    "SELECT * FROM clients WHERE fullname = ? AND product >= ?",
                    (fullname, product)
                )
                rows = self.cur.fetchone()
              
                if rows:
                    print(f"✅ Product access successful → {rows}")
                    break
              
                else:
                    print("❌ Product access failed! Try again.")
        
              
        def search_with_or():
            while True:
                product1 = input("Input product: ").strip()
                product2 = input("Second choice (Optional): ").strip()
               
                if not product1 or not product2:
                    print("❌ Choice cancelled!")
                    return
                
                self.cur.execute(
                    "SELECT * FROM clients WHERE product = ? OR product = ?",
                    (product1, product2)
                )
                rows = self.cur.fetchall()
                
                if not rows:
                    print("❌ Invalid product!")
               
                else:
                    for row in rows:
                        print(f"🎯 Product → {row[1]} | 📂 Category → {row[2]}")
                        break    
      
      
        while True:
            print("========== MENU ==========")
            print("1. View Client by ID")
            print("2. Search Client (AND)")
            print("3. Search Client (OR)")
            print("4. Exit")
            print("==========================")
              
            choice = input("Enter choice 1-4: ")
              
            if choice == "1":
                search_by_id()
                  
            elif choice == "2":
                search_with_and()
              
            elif choice == "3":
                search_with_or()
              
            elif choice == "4":
                print("Exiting program!")
                break
              
            else:     
                print("Invalid input!")       
       

def main():
  
    manager = BusinessProfileManager()
  
    while True:
        print("=== MENU ===")
        print("1. Add client")
        print("2. Show client list")
        print("3. Delete client")
        print("4. Update client")
        print("5. Advanced search")
        print("6. EXIT")
        
        choice = input("Enter choice 1-6: ")
        
        if choice == "1":
            manager.add_client()
            
        elif choice == "2":
            manager.show_clients()
        
        elif choice == "3":
            manager.delete_client()
            
        elif choice == "4":
            manager.update_client()
            
        elif choice == "5":
            manager.advanced_search()
   
        elif choice == "6":
            print("Exiting program!")
            break
        
        else:
            print("Invalid input!")


if __name__ == "__main__":
    main()

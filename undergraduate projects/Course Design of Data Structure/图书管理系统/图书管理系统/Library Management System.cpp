#include <iostream>
#include <cstdio>
#include <cstring>
#include <string>  
#include <vector>                               //vector 顺序容器 比数组优越 .at()访问
#include <algorithm>                            //模板库  
#include <fstream>
#include <cctype>                               //字符处理库   字符测试、映射
#include <iomanip>                              //流操作符头文件
using namespace std;
struct student
{
	static int s1;
	int id;//读者编号
	string name;//读者姓名
	int borrowsum;//你已借阅多少本书,默认为0
	int number;//现在还有多少本书未还，默认为0
	string borrowday;//上次借阅时间，默认为0000.00.00
	int b[10];//你所借书的的编号，最多10本
	//char bookname[100];
	string bookname;
	string authorname;
};
struct book
{
	int idnum;//图书编号号
	int BorrowCount;//图书借阅量,初始化为0
	string name;//书名
	string kind;//图书种类
	double price;//图书价格
	int sum;//图书总库存存量
	int nowsum;//图书现库存量
	string author;//图书作者
	bool ok;//是否可借,初始为可以
	string borrowdate;//图书最近一次借出时间，默认为0000-00-00；
	string returndate;//图书最近一次归还时间，默认为0000-00-00；
};
bool cmpByidnum(book a, book b)
{
	return a.idnum < b.idnum;
}
bool cmpByCount(book a, book b)
{
	return a.BorrowCount > b.BorrowCount;
}
bool cmpByBorrowsum(student a, student b)
{
	return a.borrowsum > b.borrowsum;
}
bool cmpByid(student a, student b)
{
	return a.id < b.id;
}
class Library
{
private:
	vector<book> data;
	vector<student> data1;
	vector<int> betoli;//预约书到馆，储存其编号
public:
	Library();
	void AddBook(book NewBook);  //增加图书
	void DeleteBook(string bookname, string author);//删除图书
	void BorrowBook(string name, string author);//借阅图书
	void BackBook(string name, string author, int k);//归还图书
	void ShowAllBook(); //输出系统所有图书
	void SearchBookPosWithNum(int theauthor);//按编号查询
	void  SearchBookPosWithname(string thebook); //按书名查询
	void  SearchBookPosWithAuthor(string theauthor);//按作者查询
	void  SearchBookPosWithKind(string kind);//按种类查询
	int  SearchBookPosWithAB(string theauthor, string thebook);//按作者和书名查询
	void Save();  //存入图书馆文件
	void Save1();//存入学生文件
	void printbook(book a);//输出某本书的所有信息
	void revisebook(string name, string author);//修改某本书的信息
	int SerchStudent(int id);//查询某个读者
	void AddStudent(student a);//增加一个读者
	void PrintStudent(int kid);//输出读者信息
	int GetStudent();//返回读者总数
};
Library::Library()
{
	int AllBook, AllStudent;
	ifstream fin("book.txt");
	if (fin)
	{
		fin >> AllBook;
		for (int i = 0; i < AllBook; i++)
		{
			book tem;
			fin >> tem.idnum >> tem.name >> tem.author >> tem.price >> tem.kind >> tem.sum >> tem.nowsum >> tem.BorrowCount >> tem.ok >> tem.borrowdate >> tem.returndate;
			data.push_back(tem);              //添加在数组最后
		}
		fin.close();
	}
	ifstream tfin("student.txt");
	if (tfin)
	{
		tfin >> AllStudent;
		for (int i = 0; i < AllStudent; i++)
		{
			student tem;
			tfin >> tem.id >> tem.name >> tem.borrowsum >> tem.number >> tem.borrowday;
			for (int j = 0; j < 10; j++)
			{
				tfin >> tem.b[j];
			}
			data1.push_back(tem);
		}
		tfin.close();
	}
}
int Library::GetStudent()
{
	int k = (int)data1.size();
	return k + 1;
}
void Library::AddBook(book NewBook)
{
	data.push_back(NewBook);
}
void Library::AddStudent(student newstudent)
{
	data1.push_back(newstudent);
}
void Library::DeleteBook(string bookname, string author)
{
	int pos = SearchBookPosWithAB(author, bookname);
	if (pos != -1)
	{
		data.erase(data.begin() + pos);
		Save();
		return;
	}
	else
		cout << "查无此书！\n";
}
void Library::BorrowBook(string name, string author)
{
	string BorrowDate;
	string BackDate;
	char c;
	int flag = 0;
	int sid = -1;
	for (int i = 0; i < (int)data.size(); i++)
	{
		if (data[i].name == name && data[i].author == author)
		{
			if (data[i].nowsum)
			{
				cout << "借书读者的读者号是：";
				cin >> sid;
				if (data1[sid - 1].number > 10)
				{
					cout << "现你同时借了10本书！不可再借！" << endl;
					break;
				}
				flag = 1;
				data[i].nowsum = data[i].nowsum - 1;
				data[i].BorrowCount = data[i].BorrowCount + 1;
				cout << "请输入借阅日期" << endl;
				cin >> BorrowDate;
				data[i].borrowdate = BorrowDate;
				cout << "请输入预计归还日期" << endl;
				cin >> BackDate;
				data[i].returndate = BackDate;
				data[i].ok = bool(data[i].nowsum);
				data1[sid - 1].number++;
				for (int j = 0; j < 10; j++)
				{
					if (data1[sid - 1].b[j] == 0)
						data1[sid - 1].b[j] = data[i].idnum;
					    data1[sid - 1].bookname = data[i].name.data();
					    data1[sid - 1].authorname = data[i].author;
					Save();
					Save1();
				}
				cout << "借阅成功" << endl;
			}
			else
			{
				cout << "抱歉这本书库存为零，无法借阅" << endl;
			}
		}
	}
	if (!flag)
		cout << "抱歉，未找到您要找的书。" << endl;
}
void Library::BackBook(string name, string author, int k)//k表示还书途径
{
	int c = -1;
	{
		cout << "请输入你的读者号：";
		cin >> c;
		c = c - 1;
	}
	for (int i = 0; i < (int)data.size(); i++)
	{
		if (data[i].name == name && data[i].author == author)
		{
			data[i].nowsum = data[i].nowsum + 1;
			data[i].ok = bool(data[i].nowsum);
			for (int j = 0; j < 10; j++)
			{
				if (data1[c].b[j] == data[i].idnum)
					data1[c].b[j] = 0;
			}
			data1[c].number--;
			break;
		}
	}
	Save();
	Save1();
	cout << "还书成功" << endl;
}
void Library::printbook(book a)
{

	cout << " 编号:" << setw(12) << a.idnum;
	cout << " 书名:" << setw(14) << a.name;
	cout << " 作者:" << setw(14) << a.author << endl;
	cout << " 价格:" << setw(14) << fixed << setprecision(2) << a.price;
	cout << " 种类:" << setw(14) << a.kind;
	cout << " 总库存量:" << setw(10) << a.sum;
	cout << " 现库存量:" << setw(10) << a.nowsum;
	cout << " 图书借阅量:" << setw(14) << a.BorrowCount << endl;
	cout << " 状态:" << setw(14) << (a.ok == 0 ? "不可借" : "可借");
	cout << " 近期借出日期:" << setw(14) << a.borrowdate;
	cout << " 近期归还日期:" << setw(14) << a.returndate << endl;
	cout << endl << endl;
}
void Library::PrintStudent(int kid)
{
	int id = kid - 1;
	cout << setw(8) << data1[id].id;
	cout << setw(8) << data1[id].name;
	cout << setw(18) << data1[id].number;
	if (data1[id].number)
	{
		
		cout << "                 " << endl;
		cout << "你当前借了这些书：\n";
		cout << setw(16) << "编号" << setw(16) << "书名" << setw(16) << "作者" << endl;
		for (int i = 0; i < 1; i++)
		{
			
			if (data1[id].b[i] != 0)
				cout << setw(16) << data1[id].b[i]<< setw(16) << data1[id].bookname << setw(16) << data1[id].authorname<< endl;
		}
	}
	else
		cout << "你当前并未借任何书,快去借本书看看吧！\n";
}
void Library::ShowAllBook()
{
	system("cls");
	cout << "所有图书为:" << endl;
	for (int i = 0; i < (int)data.size(); i++)
	{
		printbook(data[i]);
	}
}
int Library::SerchStudent(int id)
{
	int m = -1;
	for (int i = 0; i < (int)data1.size(); i++)
	{
		if (data1[i].id == id)
		{
			return i;
		}
	}
	return m;
}
void Library::SearchBookPosWithNum(int thenum)//按编号查询
{
	bool flag = false;
	for (int i = 0; i < (int)data.size(); i++)
	{
		if (data[i].idnum == thenum)
		{
			flag = true;
			printbook(data[i]);
		}
	}
	if (!flag) cout << "查无此编号！";
}
void Library::SearchBookPosWithname(string thebook)//按书名查询
{
	int flag = 0;
	for (int i = 0; i < (int)data.size(); i++)
	{
		if (data[i].name == thebook)
		{
			printbook(data[i]);
			flag = 1;
		}
	}
	if (!flag) cout << "查无此书！\n";
}
void Library::SearchBookPosWithAuthor(string theauthor)//按作者查询
{
	bool flag = false;
	for (int i = 0; i < (int)data.size(); i++)
	{
		if (data[i].author == theauthor)
		{
			flag = true;
			printbook(data[i]);
		}
	}
	if (!flag) cout << "查无此作者的书！";
}
void Library::SearchBookPosWithKind(string kind)//按种类查询
{
	bool flag = false;
	for (int i = 0; i < (int)data.size(); ++i)
	{
		if (data[i].kind == kind)
		{
			flag = true;
			printbook(data[i]);
		}
	}
	if (!flag) cout << "查无此类书！";
}
int Library::SearchBookPosWithAB(string theauthor, string thebook)//按作者和书名查询
{
	for (int i = 0; i < (int)data.size(); ++i)
	{
		if (data[i].author == theauthor && data[i].name == thebook)
		{
			printbook(data[i]);
			return i;
		}
	}
	cout << "查无此书！";
	return -1;
}
void Library::Save() //存入书籍文件
{
	ofstream fout("book.txt");
	if (fout)
	{
		fout << data.size() << endl;
		for (int i = 0; i < (int)data.size(); i++)
		{
			fout << data[i].idnum << " " << data[i].name << " " << data[i].author << " " << data[i].price << " " << data[i].kind /*<< " " << data[i].room */ << " " << data[i].sum << " " << data[i].nowsum << " " << data[i].BorrowCount << " " << data[i].ok/* << " " << data[i].appointment */ << " " << data[i].borrowdate << " " << data[i].returndate << " " << endl;
		}
		fout.close();
	}
}
void Library::Save1() //存入学生文件
{
	ofstream fout("student.txt");
	if (fout)
	{
		fout << data1.size() << endl;
		for (int i = 0; i < (int)data1.size(); i++)
		{
			fout << data1[i].id << " " << data1[i].name << " " << data1[i].borrowsum << " " << data1[i].number << " " << data1[i].borrowday<<endl;
			for (int j = 0; j < 10; j++)
			{
				fout << " " << data1[i].b[j]<<" "<<data1[i].bookname<<endl;
			}
			fout << endl;
		}
		fout.close();
	}
}
void Library::revisebook(string name, string author)//修改图书
{
	Library mybook;
	string  Kind;
	int num1, num2, k = 0;
	printf("你要修改的内容是：\n");
	printf("1.图书现库存量修改\n");
	printf("2.图书总库存量修改\n");
	printf("3.图书所属种类修改\n");
	printf("4.退出\n");
	for (int i = 0; i < (int)data.size(); i++)
	{
		if (data[i].author == author && data[i].name == name)
		{
			k = i;
			break;
		}
	}
	int cho;
	do
	{
		cin >> cho;
		switch (cho)
		{
		case 1:
		{
			cout << "请输入新的现库存量：\n";
			cin >> num1;
			data[k].nowsum = num1;
			Save();
			cout << "修改成功" << endl;
			break;
		}
		case 2:
		{
			cout << "请输入新的总库存量：\n";
			cin >> num2;
			data[k].sum = num2;
			Save();
			cout << "修改成功" << endl;
			break;
		}
		case 3:
		{
			cout << "请输入图书所属新种类：\n";
			cin >> Kind;
			data[k].kind = Kind;
			Save();
			cout << "修改成功" << endl;
			break;
		}
		}
	} while (cho < 3);
}

int main()
{
	cout.setf(ios::left);
	Library mybook;
	L1:cout << "************************** 欢迎使用华南理工大学图书管理系统 **************************" << endl << endl;
	cout << "请输入读者编号登录" << endl;
	int mm = 510640;
	int bh, k = 0, z = 0, cho;

	cin >> bh;
	if (bh == mm)
	{
		cout << "欢迎使用" << endl;
		k = 2;
	}
	else    z = 3;

	if (k == 2) {
		do
		{
		    L3:cout << "欢迎进入管理员系统" << endl;
			cin.clear();
			cin.sync();
			cout << " ***    1.图书目录    ***" << endl;
			cout << " ***    2.查询图书    ***" << endl;
			cout << " ***    3.添加图书    ***" << endl;
			cout << " ***    4.删除图书    ***" << endl;
			cout << " ***  5.修改图书信息  ***" << endl;
			cout << " ***      0.退出      ***" << endl;
			cout << "-------------------------------------------------------------------------------------------------------------------" << endl;
			cout << "请选择功能,输入指令 " << endl;
			cin >> cho;
			switch (cho)
			{
			case 1:
			{
				int cho2;
				mybook.ShowAllBook();
				cout << "--------------------------------------------------------------------------------------------------------------------" << endl;
				
				break;
			}
			case 2:
			{
				int p1;
				do
				{
					L2: cout << " ***       0.返回       *** " << endl;
					cout << " ***    1.按书名查询    *** " << endl;
					cout << " ***    2.按作者查询    *** " << endl;
					cout << " ***    3.按种类查询    *** " << endl;
					cout << " ***    4.按编号查询    *** " << endl;
					cout << " *** 请选择功能,输入指令 *** " << endl;
					
					string Name, Author, Kind;
					int thenum;
					cin >> p1;
					if (p1 >= 0 && p1 <= 4)
					{
						do
						{
							switch (p1)
							{
							case 1:do
							{
								cout << "请输入书名！" << endl;
								cin >> Name;
								mybook.SearchBookPosWithname(Name); //按书名查询
								break;
							} while (p1 != 0); break;
							case 2:
							{
								cout << "请输入作者！" << endl;
								cin >> Author;
								mybook.SearchBookPosWithAuthor(Author);//按作者查询
								break;
							}
							case 3:
							{
								cout << "请输入种类！" << endl;
								cin >> Kind;
								mybook.SearchBookPosWithKind(Kind);//按种类查询
								break;
							}
							case 4:
							{
								cout << "请输入编号！" << endl;
								cin >> thenum;
								mybook.SearchBookPosWithNum(thenum);//按编号查询
								break;
							}
							case 0:
							{
								goto L3;
							}
							}

						} while (p1 <= 0);

						break;
					}
					else
					{
						cout << "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" << endl;
						cout << "!!!!!!!!!!请输入正确指令!!!!!!!!!!" << endl;
						cout << "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" << endl;
						break;
					}
					
				} while (p1 >= 1 && p1 <= 4);
				goto L2;
				break;
			}
			case 3:         //增加图书
			{
				book temp;
				cin.clear();
				cin.sync();
				cout << "编号:";
				cin >> temp.idnum;
				cout << "书名:";
				cin >> temp.name;
				cout << "作者：";
				cin >> temp.author;
				cout << "价格:";
				cin >> temp.price;
				cout << "种类:";
				cin >> temp.kind;
				cout << "数量:";
				cin >> temp.sum;
				temp.nowsum = temp.sum;
				temp.BorrowCount = 0;
				temp.ok = true;
				temp.borrowdate = "0000.00.00";
				temp.returndate = "0000.00.00";
				mybook.AddBook(temp);
				mybook.Save();
				cout << "信息保存成功" << endl;
				break;
			}
			case 4:         //删除图书
			{
				string bookname, bookauthor;
				cout << "请输入书名和作者:" << endl;
				cin >> bookname >> bookauthor;
				mybook.DeleteBook(bookname, bookauthor);
				break;
			}
			case 5://修改图书信息
			{
				string name, author;
				cout << "请输入要修改的书名和作者：" << endl;
				cin >> name >> author;
				mybook.revisebook(name, author);
				break;
			}
			case 0:
			{
				goto L1;
			}
			}
		} while (cho >= 1 && cho <= 5);
		{
			cout << "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" << endl;
			cout << "!!!!!!!!!!请输入正确指令!!!!!!!!!!" << endl;
			cout << "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" << endl;
			system("pause");
		}
	}

	if (z == 3)
	{


		if (mybook.SerchStudent(bh) == -1)
		{
			int n;
			cout << "你不是此系统读者，是否注册？\n";
			cout << "                    1.注册\n";
			cout << "                    2.不需要\n";
			cin >> n;
			student temp;
			if (n == 1)
			{
				cout << "请输入你的姓名:";
				cin >> temp.name;
				cin.clear();
				cin.sync();
				temp.id = mybook.GetStudent();
				temp.borrowsum = 0;
				temp.number = 0;
				temp.borrowday = "0000.00.00";
				for (int i = 0; i < 10; i++)
				{
					temp.b[i] = 0;
				}
				mybook.AddStudent(temp);
				mybook.Save1();
				cout << "                注册成功！请记住你的读者号，若忘记请联系管理员!\n";
				cout << "                姓名:" << temp.name << endl;
				cout << "                读者号：" << temp.id << endl;
				k = temp.id;
				do
				{

					cin.clear();
					cin.sync();
					L7:cout << "***    0.返回    ***" << endl;
					cout << "***  1.查询图书  ***" << endl;
					cout << "***  2.借阅图书  ***" << endl;
					cout << "***  3.归还图书  ***" << endl;
					cout << "***4.查询读者信息***" << endl;
					cout << "***请选择功能,输入指令***" << endl;
					cin >> cho;
					int thenum;
					switch (cho)
					{
					case 1:
					{   L6:cout << " ***    0.返回    *** " << endl;
					cout << " *** 1.按书名查询 *** " << endl;
					cout << " *** 2.按作者查询 *** " << endl;
					cout << " *** 3.按种类查询 *** " << endl;
					cout << " *** 4.按编号查询 *** " << endl;
					cout << " *** 请选择功能,输入指令 *** " << endl;
					int p1;
					string Name, Author, Kind;
					cin >> p1;
					if (p1 >= 0 && p1 <= 4)
					{
						do
						{
							switch (p1)
							{
							case 1:do
							{
								cout << "请输入书名！" << endl;
								cin >> Name;
								mybook.SearchBookPosWithname(Name); //按书名查询
								break;
							} while (p1 != 0); break;
							case 2:
							{
								cout << "请输入作者！" << endl;
								cin >> Author;
								mybook.SearchBookPosWithAuthor(Author);//按作者查询
								break;
							}
							case 3:
							{
								cout << "请输入种类！" << endl;
								cin >> Kind;
								mybook.SearchBookPosWithKind(Kind);//按种类查询
								break;
							}
							case 4:
							{
								cout << "请输入编号！" << endl;
								cin >> thenum;
								mybook.SearchBookPosWithNum(thenum);//按编号查询
								break;
							}
							case 0:
							{
								goto L7;
							}
							}
						}

						while (p1 >= 1 && p1 <= 4); break;
					}
					else
					{
						cout << "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" << endl;
						cout << "!!!!!!!!!!请输入正确指令!!!!!!!!!!" << endl;
						cout << "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" << endl;
						break;
					}
					goto L6;
					break;
					}
					case 2:
					{
						string bookname, bookauthor;
						cout << "请输入要借的书名和作者：" << endl;
						cin >> bookname >> bookauthor;
						mybook.BorrowBook(bookname, bookauthor);
						mybook.Save();
						system("pause");
						break;
					}
					case 3:
					{
						string bookname, bookauthor;
						cout << "请输入要还的书名和作者：" << endl;
						cin >> bookname >> bookauthor;
						mybook.BackBook(bookname, bookauthor, -1);
						mybook.Save();
						system("pause");
						break;
					}
					case 4:
					{
						cout << setw(8) << "读者号" << setw(8) << "姓名"<< setw(8) << "现在借阅书个数" << endl;
						mybook.PrintStudent(k);
						system("pause");
						break;
					}
					case 0:
					{
						goto L1;
					}
					}
				} while (cho >= 1 && cho <= 4);
				{cout << "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" << endl;
				cout << "!!!!!!!!!!请输入正确指令!!!!!!!!!!" << endl;
				cout << "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" << endl;
				system("pause");
				}

			}
			else

				return(0);
		}


		else
		{
			k = bh;
		}

		do
		{

			cin.clear();
			cin.sync();
			L5:cout << "***    0.退出    ***" << endl;
			cout << "***  1.查询图书  ***" << endl;
			cout << "***  2.借阅图书  ***" << endl;
			cout << "***  3.归还图书  ***" << endl;
			cout << "***4.查询读者信息***" << endl;
			cout << "***请选择功能,输入指令***" << endl;
			cin >> cho;
			switch (cho)
			{
			case 1:
			{   L4:cout << " ***    0.返回    *** " << endl;
			cout << " *** 1.按书名查询 *** " << endl;
			cout << " *** 2.按作者查询 *** " << endl;
			cout << " *** 3.按种类查询 *** " << endl;
			cout << " *** 4.按编号查询 *** " << endl;
			cout << " *** 请选择功能,输入指令 *** " << endl;
			int p1;
			string Name, Author, Kind;
			int thenum;
			cin >> p1;
			if (p1 >= 0 && p1 <= 4)
			{
				do
				{
					switch (p1)
					{
					case 1:do
					{
						cout << "请输入书名！" << endl;
						cin >> Name;
						mybook.SearchBookPosWithname(Name); //按书名查询
						break;
					} while (p1 != 0); break;
					case 2:
					{
						cout << "请输入作者！" << endl;
						cin >> Author;
						mybook.SearchBookPosWithAuthor(Author);//按作者查询
						break;
					}
					case 3:
					{
						cout << "请输入种类！" << endl;
						cin >> Kind;
						mybook.SearchBookPosWithKind(Kind);//按种类查询
						break;
					}
					case 4:
					{
						cout << "请输入编号！" << endl;
						cin >> thenum;
						mybook.SearchBookPosWithNum(thenum);//按编号查询
						break;
					}
					case 0:
					{
						goto L5; 
					}
					
					}
				} while (p1 < 0);
				goto L4;
				break;
			}
			else
			{
				cout << "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" << endl;
				cout << "!!!!!!!!!!请输入正确指令!!!!!!!!!!" << endl;
				cout << "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" << endl;
				break;
			}
			goto L4;
			break;
			}
			case 2:
			{
				string bookname, bookauthor;
				cout << "请输入要借的书名和作者：" << endl;
				cin >> bookname >> bookauthor;
				mybook.BorrowBook(bookname, bookauthor);
				mybook.Save();
				system("pause");
				break;
			}
			case 3:
			{
				string bookname, bookauthor;
				cout << "请输入要还的书名和作者：" << endl;
				cin >> bookname >> bookauthor;
				mybook.BackBook(bookname, bookauthor, -1);
				mybook.Save();
				system("pause");
				break;
			}
			case 4:
			{
				cout << setw(8) << "读者号" << setw(8) << "姓名" << setw(8) << "现在借阅书个数" << endl;
				mybook.PrintStudent(k);
				system("pause");
				break;
			}
			default:
				goto L1;
			}
		} while (cho >= 1 && cho <= 4);
		{cout << "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" << endl;
		cout << "!!!!!!!!!!请输入正确指令!!!!!!!!!!" << endl;
		cout << "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" << endl;
		system("pause");
		}

	}
}

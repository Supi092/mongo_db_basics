import streamlit as st
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
client = None
db=None
def connect_to_mongo():
    global client,db
    try:
        client=MongoClient("mongodb://localhost:27017/")
        db=client['Tutort']
        st.success("Connected to Mongodb")
    except Exception:
        st.error("Failed to connect to mongodb")

def create_documents(collection_name,document):
    collection=db[collection_name]
    result=collection.insert_one(document)
    st.success(f"document inserted with ID:{result.inserted_id}")

def read_documents(collection_name):
    collection=db[collection_name]
    documents=collection.find()
    for doc in documents:
        st.json(doc)

def update_documents(collection_name,query,new_values):
    collection=db[collection_name]
    result=collection.update_one(query,{'$set':new_values})
    if result.matched_count >0:
        st.success({f"document matched:{result.matched_count}, document modified:{result.modified_count}"})
    else:
        st.warning("No documents matched the query")

def delete_documents(collection_name,query):
    collection=db[collection_name]
    result=collection.delete_one(query)
    if result.deleted_count>0:
        st.success({"Documents deleted"})
    else:
        st.warning("No documents matched the query")
#streamlit UI

st.title("Mongodb CRUD Operation")
connect_to_mongo()
operation=st.sidebar.selectbox("Select Operation",["Create","Read","Update","Delete"])
collection_name=st.text_input("Collection Name")

if operation=="Create":
    document=st.text_area("Document(Jason format)",height=200)
    if st.button("Create Document"):
        if collection_name and document:
            try:
                document=eval(document)
                create_documents(collection_name,document)
            except Exception as e:
                st.error({f"Error creating documents:{e}"})

elif operation=="Read":
    if st.button("Read Document"):
        if collection_name:
            try:
                read_documents(collection_name)
            except Exception as e:
                st.error({f"Error reading documents:{e}"})
                
elif operation == "Update":
    query = st.text_area("Query {Json Format}", height=100)
    new_values = st.text_area("New Values (Json Format)", height=100)
    if st.button("update_documents"):
        if collection_name and query and new_values:
            try:
                query=eval(query)
                new_values=eval(new_values)
                update_documents(collection_name, query, new_values)
            except Exception as e:
                st.error(f"Error updating document: {e}")

elif operation == "Delete":
    query = st.text_area("Query {Json Format}", height=100)
    if st.button("Delete Document"):
        if collection_name and query:
            try:
                query=eval(query)
                delete_documents(collection_name, query)
            except Exception as e:
                st.error(f"Error deleting document: {e}")

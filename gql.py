import requests
import json 
import argparse
from graphql import print_schema
from graphql import build_client_schema


# for api graphql instropection 
def IntrospectionQuery(endpoint, filename):

    url = endpoint
    #  for headers request
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:67.0) Gecko/20100101 Firefox/67.0", 
        "Accept": "*/*", 
        "Accept-Language": "id,en-US;q=0.7,en;q=0.3", 
        "Accept-Encoding": "gzip, deflate", 
        "content-type": "application/json"
    }

    # Post Request Query for grab schema IntrospectionQuery
    body ={"query": "query IntrospectionQuery {__schema {queryType { name },mutationType { name },subscriptionType { name },types {...FullType},directives {name,description,args {...InputValue},onOperation,onFragment,onField,locations}}}\nfragment FullType on __Type {kind,name,description,fields(includeDeprecated: true) {name,description,args {...InputValue},type {...TypeRef},isDeprecated,deprecationReason},inputFields {...InputValue},interfaces {...TypeRef},enumValues(includeDeprecated: true) {name,description,isDeprecated,deprecationReason},possibleTypes {...TypeRef}}\nfragment InputValue on __InputValue {name,description,type { ...TypeRef },defaultValue}\nfragment TypeRef on __Type {kind,name,ofType {kind,name,ofType {kind,name,ofType {kind,name}}}}"}
    data = requests.post(url, headers=headers, json=body)
    status =  data.status_code
    
    print ("\n[+] Checking endpoint ", endpoint ," .. ")
    if (status == 400) :
        print ("[+] IntrospectionQuery Now Allowed")

    if (status == 200) :
        print ("[+] IntrospectionQuery Allowed ")

        print ("[+] Saving  IntrospectionQuery to folder output .. ")
        save = (json.loads(data.text))
        filename_saved = 'output/'+filename+".json"
        with open (filename_saved, 'w') as outfile:
            json.dump(save, outfile)
        print ("[+] __schema saved in ", filename_saved)

        # Convert to client schema
        instropection = json.loads(data.text)
        client_schema = build_client_schema(instropection['data'])
        _schema = print_schema(client_schema)

        print (_schema)
        print ("[+] Saving  client_schema to folder output ..")

        client_schema_saved = 'output/'+filename+".schema"
        with open (client_schema_saved, 'w') as file:
            file.write(_schema)
        print ("[+] client_schema  saved in ", client_schema_saved)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", help="filename")
    parser.add_argument("-u", help="URL for graphql endpoint")

    argv = (parser.parse_args())
    url  = argv.u
    filename = argv.f

    if (filename != None) or (url != None):
        IntrospectionQuery(url, filename)
    else :
        print ("[!] Opps something wrong!")

if __name__ == "__main__":
    main()
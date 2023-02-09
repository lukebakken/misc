# Steps to set up Active Directory LDS

## Set up on Windows 10

Run `%SystemRoot%\ADAM\adaminstall.exe` as an adiminstrator ([source](https://dzone.com/articles/getting-started-active)).

Values I used:

* "A unique instance"
* "Instance Name": `bakken-io`
* "Yes, create an application directory partition", "Partition name": `DC=bakken,DC=io`
* Data and data recovery files: `C:\Users\Public\ADAM\bakken-io\data` (or just use the default, though it's weird to store data in `C:\Program Files`)
* "Network service account"
* "Currently logged on user"
* LDIF files: `MS-User.LDF`, `MS-UserProxy.LDF` (optional), `MS-UserProxyFull.LDF` (optional)

## Allow Anonymous Binding (option, if testing that feature)

https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2008-R2-and-2008/cc816788(v=ws.10)

## Set up Remote Server Administration Tools for Windows 10

Download: https://www.microsoft.com/en-us/download/details.aspx?id=45520

Be sure to expand and read "Install Instructions"

## Add a user and group

* Connect to your AD LDS instance
    * Run the "ADSI Edit" program using the same administrative account you used to install AD LDS.
    * "Action" -> "Connect To".
    * "Name:" - provide a name.
    * "Connection Point" -> "Select or type a Distinguished Name or Naming Context" - enter the application partition name (`DC=bakken,DC=io` in my case).
    * "Computer" -> "Select or type a domain or server" - enter either your local host name or `localhost`.
    * Click "OK".You should see the connection in the tree on the left. When you click the new node, you will see your application partition name listed as a folder. Double-clicking that shows the sub-trees that exist.

* Next, add group(s) that you will be using to test AD LDS and RabbitMQ:
    * Right-click on the `DC=bakken,DC=io` node at the top of the tree and choose "New" -> "Object".
    * Choose `organizationalUnit`, enter `groups` as the name, then choose "Finish".
    * You will see the new `OU=groups` node in the tree view.
    * Repeat the above process to create a generic `users` organizational unit.

* Add a group to the `groups` organizational unit:
    * Expand the `DC=bakken,DC=io` node at the top of the tree and right-click on `OU=groups` and choose "New" -> "Object".
    * Choose `group` and enter `rabbitmq-users`, then choose "Finish".
    * You will see the new `CN=rabbitmq-users,OU=groups,DC=bakken,DC=io` object in the right panel.

* Add a user:
    * Right-click on the `OU=users` node and choose "New" -> "Object".
    * Choose `user` and enter a full name as the value (I'm using "Luke Bakken").
    * Click "More Attributes" and choose `userPrincipalName`. Enter the name that will be used in authenticating to RabbitMQ (`lbakken`) and choose "Set". Click "OK" then "Finish" to close the dialog.
    * You will see the new `CN=` value in the right panel. Right-click it and select "Set Password". Enter a password and confirm (I used `test1234`).

* Add the user to the `rabbitmq-users` group:
    * Click on the `OU=groups` node and right-click on the `CN=rabbitmq-users` object. Choose "Properties".
    * Double-click the member property to open the editor. Choose "Add DN..." and add the fully distinguished name of the user you created. I added `CN=Luke Bakken,OU=users,DC=bakken,DC=io`.

* Verify that the user is in the group:
    * Right-click the top node in the tree view (representing the connection) and choose "New" -> "Search"
    * Enter the following search query, substituting your values as appropriate:
    ```
    (&(objectClass=user)(userPrincipalName=lbakken)(memberOf=CN=rabbitmq-users,OU=groups,DC=bakken,DC=io))
    ```
    * You should see one result in the right panel when the search is highlighted on the left.

* Verify that the user is in the group with `LDP`:
    * Run `ldp.exe` as your administrative user
    * "Connection" -> "Connect" (use defaults). You will see connection info in the right panel.
    * "Connection" -> "Bind" -> "Bind as currently logged on user" -> "OK". You will see "Authenticated as: ..." in the right panel.
    * "View" -> "Tree". Leave field blank and click "OK". You will see a tree in the left panel similar to that in ADSI editor.
    * "Browse" -> "Search". Enter the same query in "Filter", choose "Subtree" and "*" for "Attributes". When "Run" is clicked you will see one entry.

* Verify that the `in_group` query will work:
    * Run `ldp.exe` as a normal Windows user.
    * Connect using the same using the user credentials you created above (`lbakken` / `test1234`). Choose "Simple bind", then click "OK". You will see "Authenticated as: CN=..." using the `CN=` for your user.
    * "View" -> "Tree". Leave field blank and click "OK". You will see a tree in the left panel similar to that in ADSI editor.
    * If you double-click on your `DC=...,DC=...` top-level object, you will see "No children" because your user does not have permission to read objects in AD!
    * Re-open "ADSI Edit" using the same administrative account you used to install AD LDS.
    * Expand your tree, and click on `CN=Roles`
    * Right-click on `CN=Readers`, choose "Properties"
    * Find the `member` attribute, and double-click it.
    * Choose "Add DN..." and add your user in the same manner you added them to the `rabbitmq-users` group.
    * Now if you re-open `ldp.exe` you will be able to view the tree of objects and execute the same `memberOf` query that was executed above.

# Configure and start RabbitMQ

RabbitMQ configuration that will 

```
[
    {rabbit, [
        {auth_backends, [rabbit_auth_backend_ldap]},
        {loopback_users, []}
    ]},
    {rabbitmq_auth_backend_ldap, [
        {servers,             ["dsch-win"]},
        {dn_lookup_attribute, "userPrincipalName"},
        {dn_lookup_base,      "OU=users,DC=bakken,DC=io"},
        {use_ssl,             false},
        {port,                389},
        {log,                 network_unsafe},
        {resource_access_query,
            {for, [
                {resource, queue, {constant, true}},
                {resource, exchange, {constant, true}}
            ]}
        },
        {tag_queries, [{administrator, {match, {string, "${username}"}, {string, "guest"}}},
                        {management, {constant, true}}]}
        ]}
].
```

# Optional Steps

## Generate Fake Data

I used the ["Fake Name Generator"](https://www.fakenamegenerator.com/order.php) to create 65536 records to be imported into AD LDS (["Getting Me Some Data"](http://www.wictorwilen.se/how-to-use-powershell-to-populate-active-directory-with-plenty-enough-users-for-sharepoint)). Choose the following fields in this order:

* GivenName
* Surname
* StreetAddress
* City
* State
* ZipCode
* Country
* EmailAddress
* Username
* TelephoneNumber

## Modify Fake Data

The golang program `csvproc.go` will take output from the Fake Name Generator and turn it into csv suitable for import into Active Directory LDS. You will have to remove the UTF-8 bomb from the beginning of the csv file first!

```
go run ./csvproc.go 'CN=root,DC=bakken,DC=io' PATH/TO/FakeNameGenerator.com_c79fe201.csv > input.csv
```

## Import Data

On your Windows machine, run the following:

```
csvde -k -v -s localhost -i -f input.csv
```

# Links

- https://blogs.msdn.microsoft.com/robert_mcmurray/2011/09/16/ftp-and-ldap-part-2-how-to-set-up-an-active-directory-lightweight-directory-services-ad-lds-server/
- https://richmegginson.livejournal.com/25991.html
- https://msdn.microsoft.com/en-us/library/aa705903(v=vs.85).aspx
- https://msdn.microsoft.com/en-us/library/aa772136(v=vs.85).aspx
- https://technet.microsoft.com/en-us/library/ff848710.aspx
- https://msdn.microsoft.com/en-us/library/ms677604(v=vs.85).aspx
- https://msdn.microsoft.com/en-us/library/ms674942(v=vs.85).aspx
- `unicodePwd` updating: https://technet.microsoft.com/en-us/library/ff848710.aspx
- https://www.digitalocean.com/community/tutorials/how-to-configure-openldap-and-perform-administrative-ldap-tasks
- http://www.idevelopment.info/data/LDAP/LDAP_Resources/OPENLDAP_Initialize_a_New_LDAP_Directory_CentOS5.shtml
- https://docs.microsoft.com/en-us/troubleshoot/windows-server/identity/configure-ad-and-lds-event-logging
- https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2008-R2-and-2008/cc725767(v=ws.10)
- https://7thzero.com/blog/enabling-ssl-access-to-ad-lds-lightweight-directory-services

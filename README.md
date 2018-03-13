# :traffic_light:ramayana
An object oriented approach to legible production queries.
Class Domain:
  - Actor (Back-End for user-facing)
  - Reactor (Server Sessions [With UI Monitor] )
  - Entity (Archetypal discrete object)


### Aims: ###
- To develop an entity-centered class environment that use actor classes and reactor classes negotiate requests/pushes.
- To distribute a low-end-user-cost product for production teams. (reliant on cloud [airtable @$20/mo]).
- To open a channel of community development to fork into sub-industries.

#### :camel::mountain: Environment

#### Installing
##### Requirements
The ever lovely `requests` package is needed.
If you do not have `requests`, simply open a shell/cmd window and
```
$ pip install requests
```
Ramayana uses Airtable as a backend and has a nice python wrapper from @gtalarico
https://github.com/gtalarico/airtable-python-wrapper
You shouldnt have to do 
```
import vayu
```

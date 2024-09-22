# hentoid-contentv2-maker
Python GUI for making contentv2's for Hentoid

This exists as a Proof of Concept to show that someone can make the data needed for Hentoid to read manually. In its current state it reads the image files in a directory, you apply any tags you need, and it provides a relevant contentv2.json that you can place into the book folder.

Since this is a proof of concept I didn't feel the need to export as an exe yet. 

You'll need to install PySimpleGUI as well. ```python -m pip install PySimpleGUI```

For batch / mass editing please refer to https://github.com/fuwamocoanon/hentoid-contentV2-gens which works for Anchira yaml and HentaiNexus json files.

Line 139 is where the sources are listed. In the output it's called "site:" and should be the 5th line from the bottom. This determines what logo shows on the book from the library screen. If anyone wants to make it a custom field to go beyond the normal guides for the app feel free. The file below has all sites the app natively supports. Realistically, we can use this and add our own assets for custom sites as long as the header exists and can be called.
https://github.com/avluis/Hentoid/blob/master/app/src/main/java/me/devsaki/hentoid/enums/Site.java 

![image](https://github.com/user-attachments/assets/38773586-0e08-424b-b036-d505bf25198b)

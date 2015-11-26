# Collections of plugins written in Python for the Tulip graph analysis and visualization framework

That repository contains a set of Python plugins for the [Tulip framework](https://tulip.labri.fr), dedicated to the analysis and
visualization of large graphs. 

Those plugins enables to add new graph import / export process but also new graph algorithms (layout, metric, clustering, ...).
They can be called programatically or through the Tulip software graphical user interface.

The minimum version of Tulip required to use these plugins is 4.8. 
You can install it trough dedicated installers for [Windows](http://sourceforge.net/projects/auber/files/tulip/tulip-4.8.0/tulip-4.8.0_x64_setup.exe/download)
and [MacOS](http://sourceforge.net/projects/auber/files/tulip/tulip-4.8.0/Tulip-4.8.0.dmg/download) or compile it from source if you are using Linux (you can get the code source from the tulip subversion repository hosted on [sourceforge](https://sourceforge.net/p/auber/code/HEAD/tree/) or from its [github](https://github.com/anlambert/tulip) mirror.

To use the plugins, you can either:

  * load them manually through the Python Plugin editor included in the Tulip software
  * copy the repository content to the following location : `<home_directory>/.Tulip-4.8/plugins/python`, 
  the plugins will be automatically loaded when Tulip starts

  
## License

Copyright (C) 2015 Antoine Lambert

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

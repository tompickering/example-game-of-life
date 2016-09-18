# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright (C) 2016  Tom Pickering                                     #
#                                                                       #
# This program is free software: you can redistribute it and/or modify  #
# it under the terms of the GNU General Public License as published by  #
# the Free Software Foundation, either version 3 of the License, or     #
# (at your option) any later version.                                   #
#                                                                       #
# This program is distributed in the hope that it will be useful,       #
# but WITHOUT ANY WARRANTY; without even the implied warranty of        #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
# GNU General Public License for more details.                          #
#                                                                       #
# You should have received a copy of the GNU General Public License     #
# along with this program.  If not, see <http://www.gnu.org/licenses/>. #
#                                                                       #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def glider(x, y):
    return [
         (x+1, y+0),
         (x+2, y+1),
         (x+0, y+2),
         (x+1, y+2),
         (x+2, y+2),
    ]

def glider_gun(x, y):
    return [
         (x+0, y+4),
         (x+1, y+4),
         (x+0, y+5),
         (x+1, y+5),

         (x+13, y+2),
         (x+12, y+2),
         (x+11, y+3),
         (x+10, y+4),
         (x+10, y+5),
         (x+10, y+6),
         (x+11, y+7),
         (x+12, y+8),
         (x+13, y+8),

         (x+14, y+5),
         (x+15, y+3),
         (x+16, y+4),
         (x+16, y+5),
         (x+16, y+6),
         (x+15, y+7),
         (x+17, y+5),

         (x+20, y+2),
         (x+20, y+3),
         (x+20, y+4),
         (x+21, y+2),
         (x+21, y+3),
         (x+21, y+4),
         (x+22, y+1),
         (x+22, y+5),

         (x+24, y+0),
         (x+24, y+1),
         (x+24, y+5),
         (x+24, y+6),

         (x+34, y+2),
         (x+34, y+3),
         (x+35, y+2),
         (x+35, y+3),
    ]

use <card_holder.scad>
use <olivers_shapes.scad>
use <stackable_box.scad>

// Critter pieces box (x10)
//stackable_box(width=58, length=67.5, height=17);

//translate([-65,0,0]) stackable_box(width=58, length=67.5, height=17);
//translate([-65,0,15]) color("blue") stackable_box(width=58, length=67.5, height=17);

// Small card holders
// Forest location cards and special event card (x2)
//card_holder(card_width=46, card_height=65, height=32, stackable=true);
// Awards (x1)
//card_holder(card_width=46, card_height=65, height=19, stackable=true);
// Pearl Cards (x1)
//card_holder(card_width=46, card_height=65, height=15, stackable=true);
// Creature ability cards (x1)
//card_holder(card_width=46, card_height=65, height=16, stackable=true);

// Hobbit hole door thing holder (x1)
//stackable_circle_holder(width=70, length=23.5, height=17, d=14);
// Axolotol token holder
//stackable_box(width=70, length=27, height=17);

//revised above
// Hobbit hole door thing holder (x1)
//stackable_circle_holder(width=70, length=19, height=17, d=14,top=true);
// Axolotol token holder ->  marketplace token holder
//stackable_box(width=70, length=31.6, height=17,top=true);

// Holders for critter & construction cards (x2)*
//card_holder(card_width=68,card_height=94,height=32);
// and remainder
//card_holder(card_width=68,card_height=94,height=24,stackable=true);

// Holder for river destination cards
//card_holder(card_width=68,card_height=94,height=10,stackable=true);

//misc_box
//stackable_box(top=true,width=99,height=32,length=73);

//axolotl tokens?*
//stackable_box(top=true,width=15,thickness=1.5,length=39);

// VP holder
/*union () {
    stackable_box(width=55,length=63,height=32);
    difference () {
        union () {
            stackable_circle_holder(width=55, length=35, height=32, d=25);
            translate([0,33,0]) stackable_circle_holder(width=55, length=30, height=32, d=20);
        };
        translate([-1,25,0]) cube([80,20,35]);
    };
    difference() {
        union () {
            stackable_circle_holder(width=55, length=35, height=16.5, d=25,top=true);
            translate([0,33,0]) stackable_circle_holder(width=55, length=30, height=16.5, d=20,top=true);
        };
        translate([2.001,25,12.499]) cube([50.998,20,30]);
    };
};/**/
/*difference () {
    union () {
        translate([0,0,5]) stackable_circle_holder(width=73, length=35, height=25, d=25);
        stackable_box(width=73, length=35, height=32);
        cube([73,35,5]);
    };
    translate([2.001,35/2,11]) rotate([0,90,0]) cylinder(h=73-4.002,d=20);
};*/

//stackable_box(width=27.5,length=35,height=32,thickness=1.2,top=true,bottom=true);
//stackable_box(width=30,length=20,height=32,thickness=1.2,top=true,bottom=true);
//stackable_box(width=75,length=30,height=32,thickness=2,top=true,bottom=true);
stackable_box(width=75,length=57.5,height=32,thickness=2,top=true,bottom=true);


/*/box
difference() {
    translate([-2,-2,-2]) cube([288,289,72]);
    translate([-0.001,-0.001,-0.001]) cube([284.002,285.002,72]);
};

// Critter pieces box (x12)
for (y=[14.5:67.54:220]) {
    translate([226,y,0]) color("green") stackable_box(width=58, length=67.5, height=17);
    translate([226,y,15.2]) color("green") stackable_box(width=58, length=67.5, height=17);
};
for (x=[109.5:58.4:200]) {
    translate([x,217.12,0]) color("green") stackable_box(width=58, length=67.5, height=17);
    translate([x,217.12,15.2]) color("green") stackable_box(width=58, length=67.5, height=17);
}

// Small card holders
// Forest location cards and special event card (x2)
translate([51.6,0,2.002]) rotate([0,0,90]) color("green") card_holder(card_width=46, card_height=65, height=32, stackable=true);
translate([51.6,214.6,2.002]) rotate([0,0,90]) color("green") card_holder(card_width=46, card_height=65, height=32, stackable=true);
// Awards (x1)
translate([51.6,71.5,2.002]) rotate([0,0,90]) color("green") card_holder(card_width=46, card_height=65, height=19, stackable=true);
// Pearl Cards (x1)
translate([51.6,71.5,19.202]) rotate([0,0,90]) color("green") card_holder(card_width=46, card_height=65, height=15, stackable=true);
// Creature ability cards (x1)
translate([51.6,143,2.002]) rotate([0,0,90]) color("green") card_holder(card_width=46, card_height=65, height=17, stackable=true);

// Hobbit hole door thing holder (x1)
translate([51.6,143,17.202]) rotate([0,0,90]) color("green") stackable_circle_holder(width=70, length=19, height=17, d=14);
// market token holder
translate([32.2,143,17.202]) rotate([0,0,90]) color("green") stackable_box(width=70, length=31.6, height=17);

// Holder for river destination cards
translate([225,72.4,0.002]) rotate([0,0,180]) color("green") card_holder(card_width=68,card_height=94,height=10,stackable=true);
// Holders for critter & construction cards (x2)*
translate([225,145.6,0]) rotate([0,0,180]) color("green") card_holder(card_width=68,card_height=94,height=32);
translate([225,217,0]) rotate([0,0,180]) color("green") card_holder(card_width=68,card_height=94,height=32);
// and remainder
translate([225,72.4,8.202]) rotate([0,0,180]) color("green") card_holder(card_width=68,card_height=94,height=24,stackable=true);

//axolotl tokens?*
translate([265,0,2.002]) rotate([0,0,90]) color("green") stackable_box(top=true,width=15,thickness=1.5,length=39);

//misc_box
translate([125.5,0,0]) color("green") rotate([0,0,90]) stackable_box(top=true,width=99,height=32,length=73);

//VP holder
translate([53,220,0]) color("green") union () {
    stackable_box(width=55,length=63,height=32);
    difference () {
        union () {
            stackable_circle_holder(width=55, length=35, height=32, d=25);
            translate([0,33,0]) stackable_circle_holder(width=55, length=30, height=32, d=20);
        };
        translate([-1,25,0]) cube([80,20,35]);
    };
    difference() {
        union () {
            stackable_circle_holder(width=55, length=35, height=16.5, d=25,top=true);
            translate([0,33,0]) stackable_circle_holder(width=55, length=30, height=16.5, d=20,top=true);
        };
        translate([2.001,25,12.499]) cube([50.998,20,30]);
    };
};

/**/

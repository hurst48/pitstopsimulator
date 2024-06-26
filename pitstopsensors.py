from gpiozero import Button

## WHEEL CLASS
## should have attributes of GPIO sensors numbers to tell the pi which sensors to check
## these attributes should be assigned in the constructor AKA __init__


# due to the lack of toggle switches available, for testing the pushbuttons will actuate in reverse
# ie they will NOT be pressed to indicate the wheel is locked or present.
# otherwise we would need to hold the buttons down when starting (which is awkward).
REVERSE_WHEEL_BUTTONS = True


class wheel:
    """
    Class which represents the wheels
    
    
    Attributes
    ----------
    name : str
        The name of the wheel, usually front or back
        
    present : bool
        Represents whether or not the wheel is hanging on the hub
        
    locked : bool
        Represents whether or not the wheel is locked, ie if lug nut is tightened
        
    new : bool
        Represents if this is the new or old wheel
    
    valid : bool
        Represents if the wheel sensors are indicated a valid state
        Essentially, the wheel should not be indicated as locked but not present, since it needs to be present to be locked
    
    complete : bool
        Represents if the process of unlocking and removing the old wheel and placing and locking the new wheel has been finished

    
    """
    def __init__(self, name, pin_no_present, pin_no_locked, pin_no_new):
        """
        Parameters
        ----------
        name : str
            The name of the wheel, usually front or back
        
        pin_no_present : int
            The GPIO pin number of the switch indicating if the wheel is present or not
        
        pin_no_present : int
            The GPIO pin number of the switch indicating if the wheel is locked or not
        
        pin_no_new : int
            The GPIO pin number of the switch indicating if the wheel is the old one or the new one
            (this may or may not be used depending on the physical layout of the sim)
        
        """
        self.name = name ## string, rear or front, just for reference purposes
        self.present = True
        self.locked = True
        self.new = False
        self.valid = True
        self.complete = False
        
        # gpio buttons
        self.input_present = Button(pin = pin_no_present, bounce_time = 0.01)
        self.input_locked = Button(pin = pin_no_locked, bounce_time = 0.01)
        self.input_new = Button(pin = pin_no_new, bounce_time = 0.01)
        
    ## getter functions should take gpio sensors and return the relevant information
    ## for now they will just grab inputs from the command line    
    
    def update(self):
        self.locked = bool(self.input_locked.value) ^ REVERSE_WHEEL_BUTTONS
        if ((not (self.present or self.locked)) and bool(self.input_present.value)):
            self.new = True
        self.present = bool(self.input_present.value) ^ REVERSE_WHEEL_BUTTONS
        self.valid = True
        if (not self.present and self.locked):
            self.valid = False
        if self.new and self.present and self.locked:
            self.complete = True
    
    def get_present(self):
        return self.present
    def get_locked(self):
        return self.locked
    def get_valid(self):
        return self.valid
    def get_complete(self):
        return self.complete

## FUEL TANK CLASS

class fueltank:
    """
    Class representing the fuel tank
    
    Attributes
    ----------
    probe_inserted : bool
        Represents whether or not the probe is inserted
    
    level : float
        Fuel level as a % of 100
    
    full : bool
        Represents whether or not the fuel tank is full
        
    completed : bool
        Represents whether or not the fuel tank goal is complete (tank is full and fuel probe is removed)
    
    """
    # name : name of the fuel tank
    # level : float representing % of fuel in tank
    # full : bool representing if the tank is full
    # probe_inserted : bool representing if the fuel probe is inserted
    
    def __init__(self, name, pin_no_probe):
        self.name = name
        self.level = 0.0
        self.max_level = 100.0
        self.full = False
        self.probe_inserted = False
        self.input_probe = Button(pin_no_probe)
        self.complete = False
        
    def update(self):
        self.probe_inserted = bool(self.input_probe.value)
        self.level += (0.2 * int(self.probe_inserted))
        if self.level >= self.max_level:
            self.level = self.max_level
            self.full = True
    
    def get_probe(self):
        return self.probe_inserted
    def get_level(self):
        return self.level
    def get_full(self):
        return self.full
    
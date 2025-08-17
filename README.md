# Serial Dilution Tutorial Protocol

## Overview
This protocol demonstrates a **stepwise serial dilution** using the Opentrons OT-2 robot.  
It was developed following the [Python Protocol API Tutorial](https://docs.opentrons.com/v2/tutorial.html).  
The procedure preps neutralization plates with SIV (Simian immunodeficiency virus) challenged monkey serum and antibodies.  

---

## Metadata
- **Protocol Name:** Serial Dilution Tutorial  
- **API Level:** 2.13  
- **Author:** New API User  
- **Robot Type:** OT-2  

---

## Equipment & Labware

### Labware
- `opentrons_24_aluminumblock_nest_1.5ml_screwcap` (serum tubes)  
- `biorad_96_wellplate_200ul_pcr` (serum plate)  
- `nest_96_wellplate_200ul_flat` (dilution plate)  
- `corning_96_wellplate_360ul_flat` (MLV & SIV neutralization plates)  
- `opentrons_96_filtertiprack_20ul` (P20 tips)  
- `opentrons_96_tiprack_300ul` (P300 tips)  
- `nest_1_reservoir_195ml` (media reservoir)  
- `nest_12_reservoir_15ml` (virus & PBS reservoir)  

### Instruments
- `p20_single_gen2` (left mount)  
- `p300_multi_gen2` (right mount)  

---

## Protocol Steps

1. **Transfer Serum to PCR Plate**  
   Transfer 32 µL from each serum tube to the corresponding wells of a PCR plate.

2. **Add Media to Dilution Plate**  
   Transfer specified volumes of media from a reservoir to the dilution plate columns (columns 2–11).

3. **Transfer Serum to Dilution Plate**  
   Transfer 16 µL from the PCR plate to the dilution plate to initiate serial dilution.

4. **Mix and Dilute**  
   Mix columns 1–9 on the dilution plate to ensure proper dilution of serum samples.

5. **Transfer Diluted Samples to Neut Plates**  
   Dispense 25 µL from the dilution plate to MLV and SIV neutralization plates.  
   Column 11 receives 50 µL.

6. **Add Virus to Neut Plates**  
   Distribute virus solution (25 µL) to appropriate wells in the MLV and SIV plates.

7. **Add PBS**  
   Dispense PBS to the outer edges and specific wells of neutralization plates for proper controls.

8. **Incubation**  
   Plates are incubated for 1 hour before adding cells (manual step).

---

## Notes
- Multi-channel pipettes may behave differently for mixing steps; verify the tip alignment and dispense volumes.  
- Media volumes are adjusted based on serum concentration.  
- Some labware movement is performed using the robot’s gripper.  

---

## Requirements
- **Opentrons OT-2**  
- **Python API Level 2.13**  

---

## References
- Opentrons Python Protocol API Tutorial: [https://docs.opentrons.com/v2/tutorial.html](https://docs.opentrons.com/v2/tutorial.html)

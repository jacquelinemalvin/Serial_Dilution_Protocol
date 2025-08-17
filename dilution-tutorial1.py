from opentrons import protocol_api, types


metadata = {
    'apiLevel': '2.13',
    'protocolName': 'Serial Dilution Tutorial',
    'description': '''This protocol is the outcome of following the
                   Python Protocol API Tutorial located at
                   https://docs.opentrons.com/v2/tutorial.html. It takes a
                   solution and progressively dilutes it by transferring it
                   stepwise across a plate.''',
    'author': 'New API User'
}
requirements = {"robotType": "OT-2", 'apiLevel': '2.13'}

dispense_rate_multiplier = 2
aspirate_rate_multiplier = 2
num_plate_swaps = 15


# Lab Equpiment 
def run(protocol: protocol_api.ProtocolContext):
    serum_tube_rack = protocol.load_labware('opentrons_24_aluminumblock_nest_1.5ml_screwcap', 1)
    serum_plate = protocol.load_labware('biorad_96_wellplate_200ul_pcr', 2)
    dilution_plate = protocol.load_labware('nest_96_wellplate_200ul_flat', 3)

    tiprack_20ul = protocol.load_labware('opentrons_96_filtertiprack_20ul', 4)
    tiprack_300ul = protocol.load_labware('opentrons_96_tiprack_300ul', 5)
    media_reservoir = protocol.load_labware('nest_1_reservoir_195ml', 6)

    virus_reservoir = protocol.load_labware('nest_12_reservoir_15ml', 7)
    mlv_neut_plate = protocol.load_labware('corning_96_wellplate_360ul_flat', 8)
    tiprack_300ul_2 = protocol.load_labware('opentrons_96_tiprack_300ul', 9)

    siv_neut_plate = protocol.load_labware('corning_96_wellplate_360ul_flat', 10)

    mlv_neut_plates = []
    siv_neut_plates = []

    for i in range(0,num_plate_swaps):
         mlv_neut_plates.append(protocol.load_labware('corning_96_wellplate_360ul_flat', OFF_DECK))
         siv_neut_plates.append(protocol.load_labware('corning_96_wellplate_360ul_flat', OFF_DECK))

    p20 = protocol.load_instrument(
        instrument_name='p20_single_gen2',  # 20_single_gen2
        mount='left',
        tip_racks=[tiprack_20ul])

    p300_multi = protocol.load_instrument(
        instrument_name='p300_multi_gen2',  # p300_multi_gen2
        mount='right',
        tip_racks=[tiprack_300ul, tiprack_300ul_2])


    # STEP 1 Transfer monkey serum from tubes to PCR Plate
    num_wells = len(serum_tube_rack.wells())
    protocol.comment("STEP 1: Transfer serum from tubes to PCR plate\n")
    p20.transfer(
        volume=32,
        source=serum_tube_rack.rows(),
        dest=serum_plate.wells()[0:num_wells],
        new_tip='always'
    )  # Transfer from serum tube rack to serum plate.

    # Dilution plate volumes in ul
    # 4x6 -> 96 abcdefgh
    dilution_plate_media_map = [
        #   1   2   3   4   5   6   7   8   9  10  11  12
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,            # A
        0, 64, 60, 60, 60, 60, 60, 60, 60, 25, 50, 0,  # B
        0, 64, 60, 60, 60, 60, 60, 60, 60, 25, 50, 0,
        0, 64, 60, 60, 60, 60, 60, 60, 60, 25, 50, 0,
        0, 64, 60, 60, 60, 60, 60, 60, 60, 25, 50, 0,
        0, 64, 60, 60, 60, 60, 60, 60, 60, 25, 50, 0,
        0, 64, 60, 60, 60, 60, 60, 60, 60, 25, 50, 0,  # G
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0             # H
    ]
    control_dilution_plate_media_map = [
        #   1    2    3   4   5   6   7   8   9  10  11  12
        0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,            # A
        0, 64.0, 60, 60, 60, 60, 60, 60, 60, 25, 50, 0,  # B
        0, 64.0, 60, 60, 60, 60, 60, 60, 60, 25, 50, 0,
        0, 74.7, 60, 60, 60, 60, 60, 60, 60, 25, 50, 0,
        0, 74.7, 60, 60, 60, 60, 60, 60, 60, 25, 50, 0,
        0, 78.0, 60, 60, 60, 60, 60, 60, 60, 25, 50, 0,
        0, 72.0, 60, 60, 60, 60, 60, 60, 60, 25, 50, 0,  # G
        0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0             # H
    ]
    # Media amounts change based on antibody concentration


    # STEP 2 Transfer DMEM to dilution plate
    protocol.comment("\nSTEP 2: Transfer media to dilution plate\n")
    media_volumes = [64, 60, 60, 60, 60, 60, 60, 60, 70, 120]
    media_well = media_reservoir.wells()[0]
    dilution_plate_columns = dilution_plate.columns()[1:12]
    for i in range(0, 10):  # transfer media to dilution plate
        p300_multi.transfer(
            volume=media_volumes[i],
            source=media_well,
            dest=dilution_plate_columns[i]
        )


    # STEP 3
    # From each animal serum subject, transfer 16 uL into 2 separate wells on the dilution plate.
    # Second column, rows 2B - 2G.
    protocol.comment("\nSTEP 3: Transfer serum from PCR plate to dilution plate\n")
    p20.transfer(
        volume=16,
        source=serum_plate.wells()[0:3],
        dest=dilution_plate.columns()[1][1:7],  #check 1:8
        new_tip='always'
    )


    # STEP 3.5
    # Mix and dilute cols 1-9 
    protocol.comment("\nSTEP 3.5 Mix and dilute columns 1-9 of dilution plate\n")
    p300_multi.transfer(
        volume=20,
        source=dilution_plate_columns[0:-4],
        dest=dilution_plate_columns[1:-3],
        mix_before=(10, 20)
    )
    p300_multi.pick_up_tip()
    p300_multi.mix(10, 20, dilution_plate_columns[-4][0])  # WARNING multi pipette may not work as expected
    p300_multi.drop_tip()


    # STEP 4
    # Transfer dilution to siv and mlv plates
    # Dispense 25uL of DMEM into each well of each plate
    # From columns 2-10 dispense 25uL, column 11 gets 50uL
    protocol.comment("\nSTEP 4: Transfer from dilution plate to SIV and MLV Neut plates\n")
    siv_cols = siv_neut_plate.columns()[1:-1]
    last_siv_col = siv_cols.pop()
    print("SIV cols: " + str(siv_cols))

    mlv_cols = mlv_neut_plate.columns()[1:-1]
    last_mlv_col = mlv_cols.pop()
    both_neut_plate_columns = siv_cols + mlv_cols
    both_neut_plate_columns[::2] = siv_cols  # interleave lists
    both_neut_plate_columns[1::2] = mlv_cols
    dilute_cols = dilution_plate_columns[0:-2]
    dilute_cols.reverse()
    both_neut_plate_columns.reverse()
    print('neut cols: ' + str(both_neut_plate_columns))
    print('dilute cols: ' + str(dilute_cols))

    p300_multi.distribute(
        volume=25,
        source=dilution_plate_columns[-2:-1],
        dest=[last_siv_col, last_mlv_col]
    )
    # column 2-10 is 25
    p300_multi.transfer(
        volume=25,
        source=dilute_cols,
        dest=both_neut_plate_columns
    )


    #STEP 5 add 25ul to each column 2-10 from virus wells
    protocol.comment("\nSTEP 5: Transfer virus to SIV and MLV neut plates")

    p300_multi.distribute(
        volume=25,
        source=virus_reservoir.wells()[0:3],
        dest=siv_cols
    )
    p300_multi.distribute(
        volume=25,
        source=virus_reservoir.wells()[5:8],
        dest=mlv_cols
    )


    #STEP 6 Switch virus reservoir with PBS Manually. 
    # Add 100ul to outer edge of SIV and MLV plates
    protocol.comment("\nSTEP 6: Switch virus reservoir with PBS Manually. Transfer PBS to SIV and MLV neut plates ")
   
    p300_multi.distribute(
        volume=100,
        source=virus_reservoir.wells()[4],
        dest=[siv_neut_plate.columns()[11]]

    )
    p300_multi.distribute(
        volume=100,
        source=virus_reservoir.wells()[4],
        dest=[siv_neut_plate.columns()[0]]
    )

    p20.distribute(  
        volume=20,
        source=virus_reservoir.wells()[4],
        dest=[siv_cols[0][0], siv_cols[1][0], siv_cols[2][0], siv_cols[3][0], siv_cols[4][0], siv_cols[5][0],
              siv_cols[6][0], siv_cols[7][0], siv_cols[8][0]]
    )
    p300_multi.distribute(
        volume=100,
        source=virus_reservoir.wells()[4],
        dest=[mlv_neut_plate.columns()[11]]
    )

    p300_multi.distribute(
        volume=100,
        source=virus_reservoir.wells()[4],
        dest=[mlv_neut_plate.columns()[0]]
    )

    p20.distribute(
        volume=20,
        source=virus_reservoir.wells()[4],
        dest=[mlv_cols[0][0], mlv_cols[1][0], mlv_cols[2][0], mlv_cols[3][0], mlv_cols[4][0], mlv_cols[5][0],
              mlv_cols[6][0], mlv_cols[7][0], mlv_cols[8][0]]
    )

    # STEP 6 replace plates
    tiprack_300ul_3 = protocol.load_labware('opentrons_96_tiprack_300ul', protocol.OFF_DECK)
    protocol.move_labware(labware=tiprack_300ul, new_location=5, use_gripper=False)
    #incubation 1 hour, then add cells

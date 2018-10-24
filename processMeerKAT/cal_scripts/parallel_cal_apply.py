import sys
import os

import config_parser
from cal_scripts import bookkeeping
from config_parser import validate_args as va

def do_parallel_cal_apply(visname, spw, fields, calfiles):

    if len(fields.gainfields) > 1:
        fluxfile = calfiles.fluxfile
    else:
        fluxfile = calfiles.gainfile

    print " applying calibration -> primary calibrator"
    applycal(vis=visname, field=fields.fluxfield, spw = spw, selectdata=False,
            calwt=False, gaintable=[calfiles.kcorrfile, calfiles.bpassfile,
                fluxfile], gainfield=[fields.kcorrfield,
                    fields.bpassfield, fields.fluxfield], parang=True)

    print " applying calibration -> secondary calibrator"
    applycal(vis=visname, field=fields.secondaryfield, spw = spw,
            selectdata=False, calwt=False, gaintable=[calfiles.kcorrfile,
                calfiles.bpassfile, fluxfile],
            gainfield=[fields.kcorrfield, fields.bpassfield,
                fields.secondaryfield], parang=True)

    print " applying calibration -> target calibrator"
    applycal(vis=visname, field=fields.targetfield, spw = spw, selectdata=False,
            calwt=False, gaintable=[calfiles.kcorrfile, calfiles.bpassfile,
                fluxfile], gainfield=[fields.kcorrfield,
                    fields.bpassfield, fields.secondaryfield], parang=True)


if __name__ == '__main__':
    # Get the name of the config file
    args = config_parser.parse_args()

    # Parse config file
    taskvals, config = config_parser.parse_config(args['config'])

    visname = va(taskvals, 'data', 'vis', str)
    visname = os.path.split(visname.replace('.ms', '.mms'))[1]

    calfiles, caldir = bookkeeping.bookkeeping(visname)
    fields = bookkeeping.get_field_ids(taskvals['fields'])

    spw = va(taskvals, 'crosscal', 'spw', str, default='')
    refant = va(taskvals, 'crosscal', 'refant', str, default='m005')
    minbaselines = va(taskvals, 'crosscal', 'minbaselines', int, default=4)

    do_parallel_cal_apply(visname, taskvals['crosscal']['spw'], fields, calfiles,
            minbaselines, do_clearcal=True)

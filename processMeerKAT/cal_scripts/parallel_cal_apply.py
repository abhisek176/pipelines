import sys

import config_parser
from cal_scripts import bookkeeping

def do_parallel_cal_apply(visname, spw, fields, calfiles):
    print " applying calibration -> primary calibrator"
    applycal(vis=visname, field=fields.fluxfield, spw = spw, selectdata=False,
            calwt=False, gaintable=[calfiles.kcorrfile, calfiles.bpassfile,
                calfiles.fluxfile], gainfield=[fields.kcorrfield,
                    fields.bpassfield, fields.fluxfield], parang=True)

    print " applying calibration -> secondary calibrator"
    applycal(vis=visname, field=fields.secondaryfield, spw = spw,
            selectdata=False, calwt=False, gaintable=[calfiles.kcorrfile,
                calfiles.bpassfile, calfiles.fluxfile],
            gainfield=[fields.kcorrfield, fields.bpassfield,
                fields.secondaryfield], parang=True)

    print " applying calibration -> target calibrator"
    applycal(vis=visname, field=fields.targetfield, spw = spw, selectdata=False,
            calwt=False, gaintable=[calfiles.kcorrfile, calfiles.bpassfile,
                calfiles.fluxfile], gainfield=[fields.kcorrfield,
                    fields.bpassfield, fields.secondaryfield], parang=True)


if __name__ == '__main__':
    # Get the name of the config file
    args = config_parser.parse_args()

    # Parse config file
    taskvals, config = config_parser.parse_config(args['config'])

    visname = taskvals['data']['vis']
    visname = visname.replace('.ms', '.mms')

    calfiles, caldir = bookkeeping.bookkeeping(visname)
    fields = bookkeeping.get_field_ids(taskvals['fields'])

    spw = taskvals['crosscal'].pop('spw', '')
    refant = taskvals['crosscal'].pop('referenceant', 'm005')
    minbaselines = taskvals['crosscal'].pop('minbaselines', 4)

    do_parallel_cal_apply(visname, taskvals['crosscal']['spw'], fields, calfiles,
            minbaselines, do_clearcal=True)
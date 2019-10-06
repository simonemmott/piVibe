from app.api import bp
from app import vibe
from piVibe import VState
from flask import jsonify
import logging

logger = logging.getLogger(__name__)

@bp.route('/api/vibe/<state>', methods = ['GET'])
def vibe_state(state):
    logger.debug('Set vibe state: {s}'.format(s=state))
    if state == 'ON':
        logger.debug('Vibe: ON')
        vibe.on()
    if state == 'OFF':
        logger.debug('Vibe: OFF')
        vibe.off()
    if state == 'LOW':
        logger.debug('Vibe Mode: LOW')
        vibe.low()
    if state == 'MEDIUM':
        logger.debug('Vibe Mode: MEDIUM')
        vibe.medium()
    if state == 'HIGH':
        logger.debug('Vibe Mode: HIGH')
        vibe.high()
    if state == 'WAVES':
        logger.debug('Vibe Mode: WAVES')
        vibe.waves()
    return jsonify(vibe.to_dict())
    
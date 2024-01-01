# hack since pytest doesn't like absolute imports
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__)))

import boto3
from datetime import datetime
from custom_types import Draw, Matchup, Tournament, Player, Round
import uuid
from boto3.dynamodb.conditions import Key, Attr

def _get_notable_placements(draw: Draw):
    winner, runner_up, semi_finalist_1, semi_finalist_2 = None, None, None, None
    final_round = draw.rounds[-1]
    semi_finals_round = draw.rounds[-2]
    if final_round.matchups[0].winner:
        winner = { "id": final_round.matchups[0].winner.id, "name": final_round.matchups[0].winner.name }
    if final_round.matchups[0].loser:
        runner_up = { "id": final_round.matchups[0].loser.id, "name": final_round.matchups[0].loser.name }
    if semi_finals_round.matchups[0].loser:
        semi_finalist_1 = { "id ": semi_finals_round.matchups[0].loser.id, "name": semi_finals_round.matchups[0].loser.name }
    if semi_finals_round.matchups[1].loser:
        semi_finalist_2 = { "id ": semi_finals_round.matchups[1].loser.id, "name": semi_finals_round.matchups[1].loser.name }
    return { "winner": winner, "runner_up": runner_up, "semi_finalist_1": semi_finalist_1, "semi_finalist_2": semi_finalist_2 }

def _get_placement(player: Player, draw: Draw):
    num_rounds = len(draw.rounds)
    for round in draw.rounds:
        win, lose = False, False
        for matchup in round.matchups:
            if matchup.winner and player.id == matchup.winner.id:
                win = True
                break
            elif matchup.loser and player.id == matchup.loser.id:
                lose = True
                break
        if win is False and lose is False: # no data available yet
            return None
        if lose:
            round_exit = round.number # exited in "round_number" out of num_rounds
            remaining_rounds = num_rounds - round_exit
            return 2 ** remaining_rounds + 1
    return 1 # if player never lost, they won the tournament

def _create_or_update_tournament(dynamo_client, tournament: Tournament, notable_placements = None) -> str:
    """
    return the id of the tournament
    """
    tournament_table = dynamo_client.Table('Tournament')
    scan = tournament_table.scan(FilterExpression=Attr('name').eq(tournament.name).__and__(
                                                    Attr('start_date').eq(tournament.start_date.isoformat())))
    if scan['Items']:
        item = scan['Items'][0]
        if notable_placements["winner"] and notable_placements["runner_up"] and \
            "winner_id" not in item and "runner_up_id" not in item: # update winner and runner up
            tournament_table.update_item(
                Key={ 'id': item['id'] },
                UpdateExpression="set winner_id = :winner_id, winner_name = :winner_name, " + \
                    "runner_up_id = :runner_up_id, runner_up_name = :runner_up_name, " + \
                    "last_updated = :now",
                ExpressionAttributeValues={
                    'winner_id': notable_placements["winner"]["id"],
                    'winner_name': notable_placements["winner"]["name"],
                    'runner_up_id': notable_placements["runner_up"]["id"],
                    'runner_up_name': notable_placements["runner_up"]["name"],
                    ':now': datetime.utcnow().isoformat() },
                ReturnValues="UPDATED_NEW"
            )
            print("updated winner and runner up for tournament " + item['id'])
        if notable_placements["semi_finalist_1"] and notable_placements["semi_finalist_2"] and \
            "semi_finalist_1_id" not in item and "semi_finalist_2_id" not in item: # update semi finalists
            tournament_table.update_item(
                Key={ 'id': item['id'] },
                UpdateExpression="set semi_finalist_1_id = :semi_finalist_1_id, semi_finalist_1_name = :semi_finalist_1_name, " + \
                    "semi_finalist_2_id = :semi_finalist_2_id, semi_finalist_2_name = :semi_finalist_2_name, " + \
                    "last_updated = :now",
                ExpressionAttributeValues={
                    'semi_finalist_1_id': notable_placements["semi_finalist_1"]["id"],
                    'semi_finalist_1_name': notable_placements["semi_finalist_1"]["name"],
                    'semi_finalist_2_id': notable_placements["semi_finalist_2"]["id"],
                    'semi_finalist_2_name': notable_placements["semi_finalist_2"]["name"],
                    ':now': datetime.utcnow().isoformat() },
                ReturnValues="UPDATED_NEW"
            )
            print("updated semi finalists for tournament " + item['id'])
        return item['id']
    tournament_id = str(uuid.uuid4())
    tournament_item = {
        'id': tournament_id, # pk
        'name': tournament.name,
        'category': tournament.category,
        'location': tournament.location,
        'start_date': tournament.start_date.isoformat(), # sk
        'end_date': tournament.end_date.isoformat(),
        'last_updated': datetime.utcnow().isoformat()
    }
    if notable_placements["winner"] and notable_placements["runner_up"]:
        tournament_item["winner_id"] = notable_placements["winner"]["id"]
        tournament_item["winner_name"] = notable_placements["winner"]["name"]
        tournament_item["runner_up_id"] = notable_placements["runner_up"]["id"]
        tournament_item["runner_up_name"] = notable_placements["runner_up"]["name"]
    if notable_placements["semi_finalist_1"] and notable_placements["semi_finalist_2"]:
        tournament_item["semi_finalist_1_id"] = notable_placements["semi_finalist_1"]["id"]
        tournament_item["semi_finalist_1_name"] = notable_placements["semi_finalist_1"]["name"]
        tournament_item["semi_finalist_2_id"] = notable_placements["semi_finalist_2"]["id"]
        tournament_item["semi_finalist_2_name"] = notable_placements["semi_finalist_2"]["name"]
    tournament_table.put_item(Item=tournament_item)
    print("created tournament " + tournament_id)
    return tournament_id

def _create_or_update_player(dynamo_client, player: Player) -> str:
    """
    return the id of the player
    """
    player_table = dynamo_client.Table('Player')
    query = player_table.query(KeyConditionExpression=Key('id').eq(player.id))
    if query['Items']:
        # no updates performed
        item = query['Items'][0]
        return item['id']
    player_table.put_item(Item={
        'id': player.id, # pk
        'name': player.name,
        'last_updated': datetime.utcnow().isoformat()
    })
    print("created player " + player.id)
    return player.id

def _create_or_update_entrant(dynamo_client, player: Player, player_id: str, tournament_id: str, placement: int = None) -> str:
    """
    return the id of the entrant
    """
    entrant_table = dynamo_client.Table('Entrant')
    query = entrant_table.scan(FilterExpression=Attr('player_id').eq(player_id))
    if query['Items']:
        item = query['Items'][0]
        if placement and 'placement' not in item:
            # update placement and timestamp
            entrant_table.update_item(
                Key={ 'id': item['id'] },
                UpdateExpression="set placement=:placement, last_updated = :now",
                ExpressionAttributeValues={
                    ':placement': placement,
                    ':now': datetime.utcnow().isoformat()
                },
                ReturnValues="UPDATED_NEW"
            )
            print("updated entrant" + item['id'])
        return item['id']
    entrant_id = str(uuid.uuid4())
    entrant_item = {
        'id': entrant_id,
        'player_id': player_id,
        'player_name': player.name, # also available in player table
        'tournament_id': tournament_id,
        'order': player.order,
        'last_updated': datetime.utcnow().isoformat()
    }
    if placement:
        entrant_item["placement"] = placement
    entrant_table.put_item(Item=entrant_item)
    print("created entrant " + entrant_id)
    return entrant_id

def _create_or_update_matchup(dynamo_client, matchup: Matchup, round: Round, tournament_id: str):
    """
    return the id of the matchup
    """
    matchup_id = tournament_id + '-' + str(round.number) + '-' + str(matchup.order)
    matchup_table = dynamo_client.Table('Matchup')
    query = matchup_table.query(KeyConditionExpression=Key('id').eq(matchup_id),
                                FilterExpression=Attr('round_number').eq(round.number).__and__(
                                    Attr('order').eq(matchup.order)))
    if query['Items']:
        item = query['Items'][0]
        if matchup.winner and 'winner' not in item:
            # update winner_id and winner_name and timestamp
            matchup_item.update_item(
                Key={ 'id': item['id'] },
                UpdateExpression="set winner_id=:winner_id, winner_name=:winner_name, last_updated = :now",
                ExpressionAttributeValues={
                    ':winner_id': matchup.winner.id,
                    ':winner_name': matchup.winner.name,
                    ':now': datetime.utcnow().isoformat()
                },
                ReturnValues="UPDATED_NEW"
            )
            print("updated matchup " + matchup_id)
        return item['id']
    matchup_item = {
      'id': matchup_id,
      'tournament_id': tournament_id,
      'round_number': round.number,
      'round_description': round.description,
      'order': matchup.order,
      'last_updated': datetime.utcnow().isoformat()
    }
    if matchup.player1:
        matchup_item["player1_id"] = matchup.player1.id
        matchup_item["player1_name"] = matchup.player1.name # also available in player table
    if matchup.player2:
        matchup_item["player2_id"] = matchup.player2.id
        matchup_item["player2_name"] = matchup.player2.name # also available in player table
    if matchup.winner: # loser can be inferred from winner
        matchup_item['winner_id'] = matchup.winner.id
        matchup_item['winner_name'] = matchup.winner.name # also available in player table
    matchup_table.put_item(Item=matchup_item)
    print("created matchup " + matchup_id)
    return matchup_id

def _create_or_update_rounds(dynamo_client, tournament_id, rounds: list[Round]):
    """
    write all the available tournament matchups to the matchup table
    """
    for round in rounds:
        for matchup in round.matchups:
            if matchup.player1 and matchup.player2:
                _create_or_update_matchup(dynamo_client, matchup, round, tournament_id)

def create_or_update_draw(draw: Draw, session):
    """
    writes the draw to 4 tables
    
    the tournament table
        - id: UUID
        - can be looked up using tournament_name + start_date
    the players table (this is common across all tournaments)
        - id: player_id from ATP website
        - can be looked up using player_id
    the entrant table
        - id: UUID
        - can be looked up using player_id
    the matchup table
        - id: tournament_id + round_number + matchup_order
        - can be looked up using tournament_id + round_number + matchup_order
    """
    dynamo_client = session.resource('dynamodb')
    tournament_id = _create_or_update_tournament(dynamo_client, tournament=draw.tournament, notable_placements=_get_notable_placements(draw))
    for player in draw.players:
        _create_or_update_player(dynamo_client, player)
        _create_or_update_entrant(dynamo_client, player, player.id, tournament_id, _get_placement(player, draw=draw))
    _create_or_update_rounds(dynamo_client, tournament_id=tournament_id, rounds=draw.rounds)

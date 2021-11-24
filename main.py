import os
import discord
import requests
import json
from web3 import Web3
from datetime import datetime, date, timedelta
from binance import Client
######### bdaysmoothie add #########
import asyncio
from discord.ext import tasks, commands
from discord_components import *

# Binance API details
binance_api_key = "AN9W55IJhxTUjYdn1On3ko38OMWA7vVwCRV9YVqC9suMuWMymRkm63UbVrUnc5HC"
binance_secret_key = "kVMipo2B2pS8COQa4IGfoaqXNAfNaKcJPga9FE5phg5dkoZ36RO381AmaDECgYaT"
client = Client(binance_api_key, binance_secret_key, tld='us')

# Date / Time variables
date_now = datetime.now()
date_time = date_now.strftime("%Y-%m-%d %H:%M")

def get_surgefund_statistics():
    # My wallet address
    my_bsc_wallet_address = "0x89754d4b7F7F8cFD4e0D68005FFDf7dd3142C28c"



    # Define contract address
    surgefund_contract_address = "0x95c8eE08b40107f5bd70c28c4Fd96341c8eaD9c7"


    # Launch date
    surgefund_launch_date = date(2021, 8, 28)

    # Date / Time variables
    date_now = date.today()
    days_since_launch = (date_now - surgefund_launch_date).days

    # Import ABI from Smart Contract
    abi = json.loads(
        '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address[]","name":"victim","type":"address[]"},{"indexed":false,"internalType":"uint256[]","name":"claim","type":"uint256[]"}],"name":"AddVictims","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bool","name":"_canClaim","type":"bool"},{"indexed":false,"internalType":"uint256","name":"_claimWaitTime","type":"uint256"}],"name":"ChangeClaimRules","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"claimer","type":"address"},{"indexed":false,"internalType":"uint256","name":"amountBNB","type":"uint256"}],"name":"Claim","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"receiver","type":"address"},{"indexed":false,"internalType":"uint256","name":"bnbAmount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amountLeft","type":"uint256"}],"name":"DirectPayment","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bool","name":"migratedBNB","type":"bool"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"address","name":"token","type":"address"},{"indexed":false,"internalType":"address","name":"recipient","type":"address"}],"name":"FundMigration","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"timestamp","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"blockNumber","type":"uint256"}],"name":"LockedContract","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"generousUser","type":"address"},{"indexed":false,"internalType":"uint256","name":"rewardGivenUp","type":"uint256"}],"name":"OptOut","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"surgeToken","type":"address"},{"indexed":false,"internalType":"uint256","name":"donation","type":"uint256"}],"name":"SellSurgeDonation","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"newSurgeBNB","type":"address"}],"name":"SetSurgeBNBAddress","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"amountOfBNBAdded","type":"uint256"},{"indexed":false,"internalType":"address","name":"tokenDonated","type":"address"}],"name":"TokenDonation","type":"event"},{"inputs":[],"name":"LockTheContract","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address[]","name":"victims","type":"address[]"},{"internalType":"uint256[]","name":"claims","type":"uint256[]"}],"name":"addVictims","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"amountUserHasDonated","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"bnbNeededUntilPaybackComplete","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"canClaim","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"claim","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"claimWaitPeriod","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"geUnlockTime","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"isLocked","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"isTimeToClaim","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"isVictim","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"time","type":"uint256"}],"name":"lock","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bool","name":"migrateBNB","type":"bool"},{"internalType":"address","name":"token","type":"address"},{"internalType":"address","name":"recipient","type":"address"}],"name":"migrateToNewFundIfUnlocked","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"minimumClaim","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"optOut","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"paidBack","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"victim","type":"address"}],"name":"remainingBnbToClaimForVictim","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"secondsUntilNextClaim","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"}],"name":"sellAllTokenForBNB","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"}],"name":"sellAllTokenForBNBSupportingFees","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"sellSurgeBNB","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"surgeToken","type":"address"}],"name":"sellSurgeTokenForUnderlyingAsset","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"tokenBalance","type":"uint256"}],"name":"sellTokenForBNB","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"tokenBalance","type":"uint256"}],"name":"sellTokenForBNBSupportingFees","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bool","name":"_allowClaims","type":"bool"},{"internalType":"uint256","name":"_claimWaitPeriod","type":"uint256"}],"name":"setClaimRules","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_sbnb","type":"address"}],"name":"setSurgeBNBAddress","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"totalBNBDistributed","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalBNBDonated","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalShares","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"unlock","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"victim","type":"address"}],"name":"usersCurrentClaim","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"stateMutability":"payable","type":"receive"}]')

    # Create Web3 connection to Binance
    w3 = Web3(Web3.HTTPProvider('https://bsc-dataseed1.binance.org:443'))
    contract = w3.eth.contract(Web3.toChecksumAddress(surgefund_contract_address), abi=abi)

    # Retrieve details from contract function calls

    amountUserHasDonated = contract.functions.amountUserHasDonated(my_bsc_wallet_address).call()
    bnbNeededUntilPaybackComplete = float(
        w3.fromWei(contract.functions.bnbNeededUntilPaybackComplete().call(), 'ether'))
    isVictim = contract.functions.isVictim(my_bsc_wallet_address).call()
    remainingBnbToClaimForVictim = float(
        w3.fromWei(contract.functions.remainingBnbToClaimForVictim(my_bsc_wallet_address).call(), 'ether'))
    totalBNBDistributed = float(w3.fromWei(contract.functions.totalBNBDistributed().call(), 'ether'))
    totalBNBDonated = float(w3.fromWei(contract.functions.totalBNBDonated().call(), 'ether'))

    total_bnb_initial_debt = bnbNeededUntilPaybackComplete + totalBNBDonated

    current_bnb_available_in_fund = totalBNBDonated - totalBNBDistributed

    progress_of_fund_percentage = ((
                                               total_bnb_initial_debt - bnbNeededUntilPaybackComplete) / total_bnb_initial_debt) * 100
    current_return_rate = totalBNBDonated / days_since_launch

    days_until_fund_completed = bnbNeededUntilPaybackComplete / current_return_rate
    fund_completion_date = date_now + timedelta(days=days_until_fund_completed)

    # print(amountUserHasDonated)
    # print(bnbNeededUntilPaybackComplete)
    # print(isVictim)
    # print(remainingBnbToClaimForVictim)
    # print(totalBNBDistributed)
    # print(totalBNBDonated)
    # print(total_bnb_initial_debt)
    # print(current_bnb_available_in_fund)
    # print(progress_of_fund_percentage)
    # print(days_until_fund_completed)
    # print(fund_completion_date)

    message = f"""
__***Overall SurgeFund Statistics***__
```SurgeFund Launch Date: {surgefund_launch_date} ({days_since_launch} days ago)

Initial BNB Debt: {total_bnb_initial_debt} BNB

BNB Donated: {totalBNBDonated} BNB
BNB Claimed: {totalBNBDistributed} BNB 

BNB Available In Fund: {current_bnb_available_in_fund} BNB```

__***Progress Against Repayment***__
```BNB Required Until Payback Is Complete: {bnbNeededUntilPaybackComplete} BNB

Progress of SurgeFund: {round(progress_of_fund_percentage, 2)}%```

__***Fund Statistics At Current Rate (Since Launch)***__
```Average Funding Rate: {round(current_return_rate, 2)} BNB per day
Days Until Fund Payback Completion: {round(days_until_fund_completed)}
Date Of Fund Payback Completion: {fund_completion_date}```

Please send feedback or feature suggestions to @Jimmy Mc.
    """

    my_embed = discord.Embed(title=f"💰 **Overall SurgeFund Statistics** 💰", description="",
                             color=0x22B4AB)
    my_embed.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/887826128616710214/900068242180149248/SurgeFund_Icon.png")
    my_embed.add_field(name="__Report Timestamp__",
                       value=f"{date_time} BST", inline=False)
    my_embed.add_field(name="__SurgeFund Launch Date__",
                       value=f"{surgefund_launch_date} ({days_since_launch} days ago)", inline=False)
    my_embed.add_field(name="__Initial BNB Debt__", value=f"{total_bnb_initial_debt} BNB", inline=False)
    my_embed.add_field(name="__BNB Donated__", value=f"{totalBNBDonated} BNB", inline=False)
    my_embed.add_field(name="__BNB Claimed__", value=f"{totalBNBDistributed} BNB", inline=False)
    my_embed.add_field(name="__BNB Available In Fund__", value=f"{current_bnb_available_in_fund} BNB", inline=False)
    my_embed.add_field(name="__BNB Required Until Payback Is Complete__", value=f"{bnbNeededUntilPaybackComplete} BNB", inline=False)
    my_embed.add_field(name="__Progress of SurgeFund__", value=f"{round(progress_of_fund_percentage, 2)}%", inline=False)
    my_embed.add_field(name="__Average Funding Rate__", value=f"{round(current_return_rate, 2)} BNB per day", inline=False)
    my_embed.add_field(name="__Days Until Fund Payback Completion__", value=f"{round(days_until_fund_completed)}", inline=False)
    my_embed.add_field(name="__Date Of Fund Payback Completion__", value=f"{fund_completion_date}", inline=False)

    return my_embed


def get_personal_surgefund_statistics(wallet_address):
    # Define contract address
    surgefund_contract_address = "0x95c8eE08b40107f5bd70c28c4Fd96341c8eaD9c7"

    # Date / Time variables
    date_now = date.today()

    # Import ABI from Smart Contract
    abi = json.loads(
        '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address[]","name":"victim","type":"address[]"},{"indexed":false,"internalType":"uint256[]","name":"claim","type":"uint256[]"}],"name":"AddVictims","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bool","name":"_canClaim","type":"bool"},{"indexed":false,"internalType":"uint256","name":"_claimWaitTime","type":"uint256"}],"name":"ChangeClaimRules","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"claimer","type":"address"},{"indexed":false,"internalType":"uint256","name":"amountBNB","type":"uint256"}],"name":"Claim","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"receiver","type":"address"},{"indexed":false,"internalType":"uint256","name":"bnbAmount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amountLeft","type":"uint256"}],"name":"DirectPayment","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bool","name":"migratedBNB","type":"bool"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"address","name":"token","type":"address"},{"indexed":false,"internalType":"address","name":"recipient","type":"address"}],"name":"FundMigration","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"timestamp","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"blockNumber","type":"uint256"}],"name":"LockedContract","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"generousUser","type":"address"},{"indexed":false,"internalType":"uint256","name":"rewardGivenUp","type":"uint256"}],"name":"OptOut","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"surgeToken","type":"address"},{"indexed":false,"internalType":"uint256","name":"donation","type":"uint256"}],"name":"SellSurgeDonation","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"newSurgeBNB","type":"address"}],"name":"SetSurgeBNBAddress","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"amountOfBNBAdded","type":"uint256"},{"indexed":false,"internalType":"address","name":"tokenDonated","type":"address"}],"name":"TokenDonation","type":"event"},{"inputs":[],"name":"LockTheContract","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address[]","name":"victims","type":"address[]"},{"internalType":"uint256[]","name":"claims","type":"uint256[]"}],"name":"addVictims","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"amountUserHasDonated","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"bnbNeededUntilPaybackComplete","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"canClaim","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"claim","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"claimWaitPeriod","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"geUnlockTime","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"isLocked","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"isTimeToClaim","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"isVictim","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"time","type":"uint256"}],"name":"lock","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bool","name":"migrateBNB","type":"bool"},{"internalType":"address","name":"token","type":"address"},{"internalType":"address","name":"recipient","type":"address"}],"name":"migrateToNewFundIfUnlocked","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"minimumClaim","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"optOut","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"paidBack","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"victim","type":"address"}],"name":"remainingBnbToClaimForVictim","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"secondsUntilNextClaim","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"}],"name":"sellAllTokenForBNB","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"}],"name":"sellAllTokenForBNBSupportingFees","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"sellSurgeBNB","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"surgeToken","type":"address"}],"name":"sellSurgeTokenForUnderlyingAsset","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"tokenBalance","type":"uint256"}],"name":"sellTokenForBNB","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"tokenBalance","type":"uint256"}],"name":"sellTokenForBNBSupportingFees","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bool","name":"_allowClaims","type":"bool"},{"internalType":"uint256","name":"_claimWaitPeriod","type":"uint256"}],"name":"setClaimRules","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_sbnb","type":"address"}],"name":"setSurgeBNBAddress","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"totalBNBDistributed","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalBNBDonated","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalShares","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"unlock","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"victim","type":"address"}],"name":"usersCurrentClaim","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"stateMutability":"payable","type":"receive"}]')

    # Create Web3 connection to Binance
    w3 = Web3(Web3.HTTPProvider('https://bsc-dataseed1.binance.org:443'))
    contract = w3.eth.contract(Web3.toChecksumAddress(surgefund_contract_address), abi=abi)

    # Retrieve details from contract function calls

    amountUserHasDonated = contract.functions.amountUserHasDonated(wallet_address).call()
    bnbNeededUntilPaybackComplete = float(
        w3.fromWei(contract.functions.bnbNeededUntilPaybackComplete().call(), 'ether'))

    isVictim = contract.functions.isVictim(wallet_address).call()
    remainingBnbToClaimForVictim = float(
        w3.fromWei(contract.functions.remainingBnbToClaimForVictim(wallet_address).call(), 'ether'))
    totalBNBDistributed = float(w3.fromWei(contract.functions.totalBNBDistributed().call(), 'ether'))
    totalBNBDonated = float(w3.fromWei(contract.functions.totalBNBDonated().call(), 'ether'))
    current_bnb_available_in_fund = totalBNBDonated - totalBNBDistributed
    usersCurrentClaim = float(w3.fromWei(contract.functions.usersCurrentClaim(wallet_address).call(), 'ether'))

    current_bnb_price = float(client.get_symbol_ticker(symbol="BNBUSD")["price"])

    value_of_current_bnb_available_in_fund = current_bnb_available_in_fund * current_bnb_price
    value_of_current_claim = usersCurrentClaim * current_bnb_price

    current_bnb_in_fund_vs_debt_percentage = get_percentage(current_bnb_available_in_fund, bnbNeededUntilPaybackComplete)
    claim_vs_overall_debt_percentage = get_percentage(remainingBnbToClaimForVictim, bnbNeededUntilPaybackComplete)
    claim_vs_available_bnb_percentage = get_percentage(usersCurrentClaim, current_bnb_available_in_fund)

    # print(amountUserHasDonated)
    # print(bnbNeededUntilPaybackComplete)
    # print(isVictim)
    # print(remainingBnbToClaimForVictim)
    # print(totalBNBDistributed)
    # print(totalBNBDonated)
    # # print(total_bnb_initial_debt)
    # print(current_bnb_available_in_fund)
    # # print(progress_of_fund_percentage)
    # # print(days_until_fund_completed)
    # # print(fund_completion_date)
    # print(current_bnb_price)
    # print(value_of_current_claim)
    # print(value_of_current_bnb_available_in_fund)

    my_embed = discord.Embed(title="💰 **Your SurgeFund Claim Details** 💰", description="", color=0x22B4AB)
    my_embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/887826128616710214/900068242180149248/SurgeFund_Icon.png")
    my_embed.add_field(name="__BNB yet to be repaid to all victims__", value=f"{bnbNeededUntilPaybackComplete} BNB", inline=False)
    my_embed.add_field(name="__BNB you have left to claim__", value=f"{remainingBnbToClaimForVictim} BNB", inline=False)
    my_embed.add_field(name="__BNB currently available in SurgeFund__", value=f"{current_bnb_available_in_fund} BNB", inline=False)
    my_embed.add_field(name="__BNB that you can claim now__", value=f"{usersCurrentClaim} BNB", inline=False)
    my_embed.add_field(name="__Current price per BNB__", value=f"${current_bnb_price}", inline=False)
    my_embed.add_field(name="__Value of your current BNB claim__", value=f"${round(value_of_current_claim, 2)}", inline=False)
    my_embed_disclaimer_text = f"💰 The total BNB currently available in the SurgeFund is {round(current_bnb_in_fund_vs_debt_percentage, 3)}% of the remaining BNB yet to be paid to all victims."
    my_embed_disclaimer_text += f"\n\n💰 The BNB that you have left to claim is {round(claim_vs_overall_debt_percentage, 3)}% of the overall BNB debt outstanding."
    my_embed_disclaimer_text += f"\n\n💰 The BNB that you can claim now is {round(claim_vs_available_bnb_percentage, 3)}% of the current BNB in the SurgeFund."
    my_embed.set_footer(text=my_embed_disclaimer_text)

    return my_embed


def createCustomHelpEmbedMessage():
    embed = discord.Embed(
        title="Available SurgeFund Tracker Bot Commands",
        description="Here are all the available commands for the SurgeFund Tracker Bot.",
        color=0x22B4AB)
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/887826128616710214/900068242180149248/SurgeFund_Icon.png")
    embed.add_field(name="surgefund, Surgefund, $surgefund, $Surgefund",
                    value="Provides a summary of the current SurgeFund statistics.",
                    inline=False)
    embed.add_field(name="mysurgefund, Mysurgefund, $mysurgefund, $Mysurgefund",
                    value="This provides a summary of your personal SurgeFund claim statistics.  You will be prompted to provide your public BEP-20 wallet address prior tp the summary being provided.",
                    inline=False)
    return embed


def get_percentage(x, y):
    percentage = (x / y) * 100
    return percentage




bot = commands.Bot(command_prefix='', help_command=None)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    DiscordComponents(bot)


# @bot.command(aliases=['Mysurgefund', '$mysurgefund', '$Mysurgefund'])
@bot.command(aliases=['Mysurgefund', '$mysurgefund', '$Mysurgefund'])
@commands.dm_only()
async def mysurgefund(ctx):
    wallet_message = 'Please enter your Public BEP-20 wallet address:'
    await ctx.author.send(wallet_message)

    def check_message(msg):
        return msg.author == ctx.author and len(msg.content) > 0

    try:
        wallet_address = await bot.wait_for("message", check=check_message, timeout=30)  # 30 seconds to reply
    except asyncio.TimeoutError:
        await ctx.author.send("Sorry, you either didn't reply with your wallet address or didn't reply in time.  Please call the $mysurgefund command again.")
        return

    try:
        checksum_wallet_address = Web3.toChecksumAddress(wallet_address.content)
        print(checksum_wallet_address)
        personal_surge_fund_statistics = get_personal_surgefund_statistics(checksum_wallet_address)
    except Exception as e:
        print(e)
        await ctx.author.send("Sorry you didn't enter a valid Public BEP-20 wallet address.  Please call the $mysurgefund command again.")
        return

    await ctx.author.send(embed=personal_surge_fund_statistics)

@bot.command(aliases=['Surgefund', '$surgefund', '$Surgefund'])
@commands.dm_only()
async def surgefund(ctx):
    surge_fund_statistics = get_surgefund_statistics()
    await ctx.author.send(embed=surge_fund_statistics)


@bot.command(aliases=['Help', '$help', '$Help'])
@commands.dm_only()
async def help(ctx):
    help_embed = createCustomHelpEmbedMessage()
    await ctx.author.send(embed=help_embed)

# Live bot
bot.run("ODk5NTY3NTI5MDEyMzg3OTIw.YW0pjA.YvSHuXWBAvTdKK79Jj5ofOLvegw")

# Test bot
# bot.run("ODk5OTY1NDkwNzU4Mjk1NjAy.YW6cLQ.iaBvDMK9UefdJjN7iwx3DdFTyaM")
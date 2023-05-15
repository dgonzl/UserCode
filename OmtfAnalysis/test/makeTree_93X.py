import FWCore.ParameterSet.Config as cms
import commands
import os

#from Configuration.StandardSequences.Eras import eras
#process = cms.Process('OmtfTree',eras.Run2_2016)

process = cms.Process('OmtfTree')

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )

#
# For processing single files insert lines with 'file:/PATH/FILE.root'
# alernatively one can use 'root://xrootd.unl.edu//store/express/Run2015A.....root'
# or                       '/store/express/Run2015A/ExpressPhysics/FEVT/...root'
# (there is 255 file limit though). Can be empty for crab.
#
process.source = cms.Source("PoolSource", 
fileNames = cms.untracked.vstring(
'/store/mc/PhaseIIFall17D/SingleMu_FlatPt-2to100/GEN-SIM-DIGI-RAW/L1TPU140_93X_upgrade2023_realistic_v5-v1/00000/54C9CCAA-AA3A-E811-BEB7-06480E0002BB.root'
),
inputCommands=cms.untracked.vstring(
        'keep *',
        'drop l1tEMTFHit2016Extras_simEmtfDigis_CSC_HLT',
        'drop l1tEMTFHit2016Extras_simEmtfDigis_RPC_HLT',
        'drop l1tEMTFHit2016s_simEmtfDigis__HLT',
        'drop l1tEMTFTrack2016Extras_simEmtfDigis__HLT',
        'drop l1tEMTFTrack2016s_simEmtfDigis__HLT')
)

#
# import of standard configurations
#
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
#process.load('Configuration.EventContent.EventContent_cff')
#process.load('Configuration.Geometry.GeometryExtended2016Reco_cff')
#process.load('Configuration.Geometry.GeometryDB_cff')
process.load('Configuration.Geometry.GeometryExtended2017Reco_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.load('Configuration.StandardSequences.RawToDigi_Data_cff')
process.load('EventFilter.L1TRawToDigi.bmtfDigis_cfi')
process.load('EventFilter.L1TRawToDigi.emtfStage2Digis_cfi')
process.load('EventFilter.L1TRawToDigi.gmtStage2Digis_cfi')
process.load('EventFilter.L1TXRawToDigi.twinMuxStage2Digis_cfi')
process.load('EventFilter.L1TRawToDigi.omtfStage2Digis_cfi')
#process.load('EventFilter.L1TRawToDigi.omtfStage2Raw_cfi')
#process.load('EventFilter.L1TRawToDigi.caloLayer1Digis_cfi')
process.load('EventFilter.L1TRawToDigi.caloStage2Digis_cfi')
#process.load("CondTools/RPC/RPCLinkMap_sqlite_cff")


#
# set proper GlobalTag
#
#process.GlobalTag.globaltag = 'FT_R_53_V10::All' #rereco 2012ABC
#process.GlobalTag.globaltag = 'FT_R_53_V18::All' #rereco 2012ABC
#process.GlobalTag.globaltag = 'FT_R_53_V21::All' #rereco 2012D
#process.GlobalTag.globaltag  = 'GR_E_V46::All' #rereco
#process.GlobalTag.globaltag  = 'GR_P_V50::All' #rereco
#process.GlobalTag.globaltag  = 'GR_P_V54::All' #rereco
#process.GlobalTag.globaltag  = 'GR_P_V56::All' #rereco
#process.GlobalTag.globaltag  = '74X_dataRun2_Prompt_v0'
#process.GlobalTag.globaltag  = '74X_dataRun2_Express_v0'
#process.GlobalTag.globaltag  = 'auto:run2_data'
#process.GlobalTag.globaltag  = '80X_dataRun2_Prompt_v8'
from Configuration.AlCa.GlobalTag import GlobalTag
#from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_data', '')
#process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc', '')
#process.GlobalTag.globaltag  = '92X_dataRun2_Prompt_v4'
#process.GlobalTag.globaltag = '100X_dataRun2_v1'
#process.GlobalTag.globaltag = '100X_dataRun2_Express_v3'
#process.GlobalTag.globaltag = '101X_dataRun2_Express_v8'9
#process.GlobalTag.globaltag = '93X_upgrade2023_realistic_v5'
process.GlobalTag.globaltag = '102X_mcRun2_asymptotic_v3'
#
# message logger
#
process.load('FWCore.MessageService.MessageLogger_cfi')
#process.MessageLogger.cerr.threshold = cms.untracked.string('DEBUG')
#process.MessageLogger.debugModules.append('muonRPCDigis')
#process.MessageLogger.debugModules.append('omtfStage2Digis')
#process.MessageLogger.debugModules.append('omtfStage2Raw')
#process.MessageLogger.debugModules.append('omtfStage2Digis2')
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1000)
process.MessageLogger.suppressWarning  = cms.untracked.vstring('Geometry', 'AfterSource','L1T','L1GlobalTriggerRawToDigi')
process.options = cms.untracked.PSet( wantSummary=cms.untracked.bool(False))

process.digiComapre = cms.EDAnalyzer("OmtfDigiCompare",
  srcRPC_OMTF = cms.InputTag('omtfStage2Digis'),
#  srcRPC_OMTF = cms.InputTag('omtfStage2Digis2','OmtfUnpacker2'),
  srcRPC_PACT = cms.InputTag('muonRPCDigis'),

  srcCSC_OMTF = cms.InputTag('omtfStage2Digis'),
#  srcCSC_OMTF  = cms.InputTag('omtfStage2Digis2','OmtfUnpacker2'),
#  srcCSC_CSC = cms.InputTag('csctfDigis'),
  srcCSC_CSC = cms.InputTag('emtfStage2Digis'),

  srcOMTF_DATA = cms.InputTag('omtfStage2Digis'),
  srcOMTF_EMUL = cms.InputTag('gmtStage2Digis','OMTF'),
#  srcOMTF_EMUL = cms.InputTag('omtfEmulator','OMTF'),
#
#  srcDTPh_BMTF = cms.InputTag('bmtfDigis'),
#  srcDTTh_BMTF = cms.InputTag('bmtfDigis'),
  srcDTPh_BMTF = cms.InputTag('twinMuxStage2Digis','PhIn'),
  srcDTTh_BMTF = cms.InputTag('twinMuxStage2Digis','ThIn'),
  srcDTPh_OMTF = cms.InputTag('omtfStage2Digis'),
  srcDTTh_OMTF = cms.InputTag('omtfStage2Digis'),
#  srcDTPh_OMTF = cms.InputTag('omtfStage2Digis2','OmtfUnpacker2'),
#  srcDTTh_OMTF = cms.InputTag('omtfStage2Digis2','OmtfUnpacker2'),
)

process.omtfStage2Raw = cms.EDProducer("OmtfPacker",
  rpcInputLabel = cms.InputTag('omtfStage2Digis'),
  cscInputLabel = cms.InputTag('omtfStage2Digis'),
  dtPhInputLabel = cms.InputTag('omtfStage2Digis'),
  dtThInputLabel = cms.InputTag('omtfStage2Digis'),
)

process.omtfStage2Digis2 = cms.EDProducer("OmtfUnpacker",
  inputLabel = cms.InputTag('omtfStage2Raw'),
  useRpcConnectionFile = cms.bool(True),
  rpcConnectionFile = cms.string("CondTools/RPC/data/RPCOMTFLinkMapInput.txt"),
  outputTag = cms.string("OmtfUnpacker2"),
)

#
###OMTF emulator configuration
#
#OMTF ESProducer. Fills CondFormats from XML files.
process.omtfParamsSource = cms.ESSource( "EmptyESSource",
     recordName = cms.string('L1TMuonOverlapParamsRcd'),
    iovIsRunNotTime = cms.bool(True),
    firstValid = cms.vuint32(1)
)
process.omtfParams = cms.ESProducer( "L1TMuonOverlapParamsESProducer",
     patternsXMLFiles = cms.VPSet( cms.PSet(patternsXMLFile = cms.FileInPath("L1Trigger/L1TMuon/data/omtf_config/Patterns_0x0003.xml")),),
     configXMLFile = cms.FileInPath("L1Trigger/L1TMuon/data/omtf_config/hwToLogicLayer_0x0006.xml"),
)

import L1Trigger.L1TMuonOverlap.simOmtfDigis_cfi
process.omtfEmulator=L1Trigger.L1TMuonOverlap.simOmtfDigis_cfi.simOmtfDigis.clone() 
process.omtfEmulator.srcDTPh = cms.InputTag('omtfStage2Digis')
process.omtfEmulator.srcDTTh = cms.InputTag('omtfStage2Digis')
process.omtfEmulator.srcCSC = cms.InputTag('omtfStage2Digis')
process.omtfEmulator.srcRPC = cms.InputTag('omtfStage2Digis')
#process.omtfEmulator.dropRPCPrimitives = cms.bool(False)
#process.omtfEmulator.dropDTPrimitives = cms.bool(False)
#process.omtfEmulator.dropCSCPrimitives = cms.bool(False)
process.omtfEmulator.dumpResultToXML = cms.bool(False)
process.omtfEmulator.bxMin = cms.int32(0)
process.omtfEmulator.bxMax = cms.int32(0)

process.omtfEmulator = cms.EDProducer("L1TMuonOverlapTrackProducer",
                                      srcDTPh = cms.InputTag('simDtTriggerPrimitiveDigis'),
                                      srcDTTh = cms.InputTag('simDtTriggerPrimitiveDigis'),
                                      srcCSC = cms.InputTag('simCscTriggerPrimitiveDigis','MPCSORTED'),
                                      srcRPC = cms.InputTag('simMuonRPCDigis'), 
                                      dumpResultToXML = cms.bool(False),
                                      dumpDetailedResultToXML = cms.bool(False),
                                      XMLDumpFileName = cms.string("TestEvents.xml"),
                                      dumpGPToXML = cms.bool(False),
                                      readEventsFromXML = cms.bool(False),
                                      eventsXMLFiles = cms.vstring("TestEvents.xml"),
                                      dropRPCPrimitives = cms.bool(False),
                                      dropDTPrimitives = cms.bool(False),
                                      dropCSCPrimitives = cms.bool(False),
                                      bxMin = cms.int32(0),
                                      bxMax = cms.int32(0)
)

#
# reemulate GMT, with changed OMTF
#
process.emulGmtCaloSumDigis = cms.EDProducer('L1TMuonCaloSumProducer',
    caloStage2Layer2Label = cms.InputTag("caloStage2Digis",'CaloTower'),
)
process.emulGmtStage2Digis = cms.EDProducer('L1TMuonProducer',
    barrelTFInput  = cms.InputTag("gmtStage2Digis", "BMTF"),
    overlapTFInput = cms.InputTag("omtfEmulator", "OMTF"),
#    overlapTFInput = cms.InputTag("gmtStage2Digis", "OMTF"),
    forwardTFInput = cms.InputTag("gmtStage2Digis", "EMTF"),
    #triggerTowerInput = cms.InputTag("simGmtCaloSumDigis", "TriggerTower2x2s"),
    triggerTowerInput = cms.InputTag("emulGmtCaloSumDigis", "TriggerTowerSums"),
    autoBxRange = cms.bool(True), # if True the output BX range is calculated from the inputs and 'bxMin' and 'bxMax' are ignored
    bxMin = cms.int32(-3),
    bxMax = cms.int32(4),
    autoCancelMode = cms.bool(False), # if True the cancel out methods are configured depending on the FW version number and 'emtfCancelMode' is ignored
    emtfCancelMode = cms.string("coordinate") # 'tracks' or 'coordinate'
)


process.raw2digi_step = cms.Path(process.muonRPCDigis+process.csctfDigis+process.bmtfDigis+process.emtfStage2Digis+process.twinMuxStage2Digis+process.gmtStage2Digis+process.caloStage2Digis)
#process.raw2digi_step = cms.Path(process.muonRPCDigis)
process.omtf_step = cms.Path(process.omtfStage2Digis+process.omtfEmulator+process.emulGmtCaloSumDigis+process.emulGmtStage2Digis)
#process.omtf_step = cms.Path(process.omtfStage2Digis+process.omtfStage2Raw+process.omtfStage2Digis2+process.digiComapre+process.omtfEmulator+process.emulGmtCaloSumDigis+process.emulGmtStage2Digis)
#process.omtf_step = cms.Path(process.omtfStage2Digis+process.omtfStage2Raw+process.omtfStage2Digis2)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.schedule = cms.Schedule(process.raw2digi_step, process.omtf_step, process.endjob_step)

#
# OMTF tree 
#
process.omtfTree = cms.EDAnalyzer("OmtfTreeMaker",
  histoFileName = cms.string("omtfHelper.root"),
  treeFileName = cms.string("omtfTree.root"),

  menuInspector = cms.PSet( 
#    namesCheckHltMuMatch = cms.vstring(
#      "HLT_IsoMu22_v","HLT_IsoTkMu22_v","HLT_Mu50_v","HLT_TkMu50_v","HLT_Mu45_eta2p1_v",
#      "HLT_IsoMu22_eta2p1_v", "HLT_IsoMu24_v", "HLT_IsoMu27_v",
#      "HLT_IsoTkMu22_eta2p1_v", "HLT_IsoTkMu24_v", "HLT_IsoTkMu27_v",
#      "HLT_Mu55_v", "HLT_IsoMu24_eta2p1_v", "HLT_IsoTkMu24_eta2p1_v"
#    ),
    namesCheckHltMuMatch = cms.vstring(
      "HLT_IsoMu20_v","HLT_IsoMu24_v","HLT_IsoMu27_v"
    ),
  ),

   linkSynchroGrabber = cms.PSet(
     rawSynchroTag = cms.InputTag("muonRPCDigis"),
     writeHistograms = cms.untracked.bool(True),
     deltaR_MuonToDetUnit_cutoff = cms.double(0.3),
     checkInside = cms.bool(True),
     linkMonitorPSet = cms.PSet(
       useFirstHitOnly = cms.untracked.bool(True),
       dumpDelays = cms.untracked.bool(True) # set to True for LB delay plots
     ),
     synchroSelector = cms.PSet(
       checkRpcDetMatching_minPropagationQuality = cms.int32(0),
       checkRpcDetMatching_matchingScaleValue = cms.double(3),
       checkRpcDetMatching_matchingScaleAuto  = cms.bool(True),
       checkUniqueRecHitMatching_maxPull = cms.double(2.),
       checkUniqueRecHitMatching_maxDist = cms.double(5.)
     )
   ),
  
  l1ObjMaker = cms.PSet(
    omtfEmulSrc = cms.InputTag('omtfEmulator','OMTF',"OmtfTree"),
    omtfDataSrc = cms.InputTag('omtfStage2Digis'),
#   omtfDataSrc = cms.InputTag('gmtStage2Digis','OMTF'),
    emtfDataSrc = cms.InputTag('gmtStage2Digis','EMTF'),
    bmtfDataSrc = cms.InputTag('gmtStage2Digis','BMTF'),
    gmtDataSrc = cms.InputTag('gmtStage2Digis','Muon'),
    gmtEmulSrc = cms.InputTag('emulGmtStage2Digis',''),
  ),
  genObjectFinder = cms.PSet(
    genColl = cms.InputTag("genParticles")
  ),                                 
  closestTrackFinder = cms.PSet(
    trackColl = cms.InputTag("generalTracks")
  ),

  onlyBestMuEvents = cms.bool(False),
  bestMuonFinder = cms.PSet(
    muonColl = cms.InputTag("muons"),
    beamSpot = cms.InputTag("offlineBeamSpot"),
    requireInnerTrack = cms.bool(True),
    requireOuterTrack = cms.bool(False),
    requireGlobalTrack = cms.bool(False),
    requireLoose       = cms.bool(True),
    minPt = cms.double(3.),
    maxTIP = cms.double(0.2),
    maxAbsEta = cms.double(2.4),
    minNumberTrackerHits = cms.int32(6),
    minNumberRpcHits = cms.int32(0),
    minNumberDtCscHits = cms.int32(0),
    minNumberOfMatchedStations = cms.int32(0),
    cutTkIsoRel = cms.double(0.1),
    cutPFIsoRel = cms.double(0.15),
    deltaPhiUnique = cms.double(1.0),
    deltaEtaUnique = cms.double(0.5),
    minPtUnique = cms.double(2.0),
    looseUnique = cms.bool(True)
  ),
)

#
# refit Muon
#
#process.load("TrackingTools.RecoGeometry.RecoGeometries_cff")
#process.load("TrackingTools.TrackRefitter.TracksToTrajectories_cff")
#process.load("TrackingTools.TrackRefitter.globalMuonTrajectories_cff")
#import TrackingTools.TrackRefitter.globalMuonTrajectories_cff
#process.refittedMuons = TrackingTools.TrackRefitter.globalMuonTrajectories_cff.globalMuons.clone()
#process.refittedMuons*
process.OmtfTree = cms.Path(process.omtfTree)
process.schedule.append(process.OmtfTree)

#print process.dumpPython();
print process.schedule


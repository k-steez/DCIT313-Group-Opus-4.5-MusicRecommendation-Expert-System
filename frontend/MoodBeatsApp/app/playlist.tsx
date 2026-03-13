import { View, Text, StyleSheet, TouchableOpacity, ScrollView, Image } from 'react-native';
import React from 'react';
import { router } from 'expo-router';
import { LinearGradient } from 'expo-linear-gradient';
import { Feather } from '@expo/vector-icons';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useStore } from '../store/useStore';

// Removed the mock playlist since we use the real one

export default function PlaylistScreen() {
  const { playlist, mood, activity, lyricPreference } = useStore();
  
  // Format preference labels
  const getLyricLabel = (pref: string) => {
    switch (pref) {
      case 'with_lyrics': return 'With Lyrics';
      case 'instrumental': return 'Instrumental';
      default: return 'No Preference';
    }
  };
  return (
    <LinearGradient 
      colors={['#ffffff', '#fcf8ff', '#fdfaff']} 
      style={styles.container}
    >
      <SafeAreaView style={styles.safeArea}>
        
        {/* Header */}
        <View style={styles.header}>
          <TouchableOpacity 
            style={styles.iconButton}
            onPress={() => router.push('/home')} // Route back to the beginning for standard flow
          >
            <Feather name="chevron-left" size={24} color="#374151" />
          </TouchableOpacity>
          <Text style={styles.headerTitle}>Your Playlist</Text>
          <TouchableOpacity style={styles.iconButton}>
            <Feather name="refresh-cw" size={20} color="#374151" />
          </TouchableOpacity>
        </View>

        {/* Scroll Content */}
        <ScrollView 
          showsVerticalScrollIndicator={false}
          contentContainerStyle={styles.scrollContent}
        >
          {/* Summary Card */}
          <LinearGradient
            colors={['#FFB703', '#F97316']}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 1 }}
            style={styles.summaryCard}
          >
            <Text style={styles.summaryTitle}>Your MoodBeats Playlist</Text>
            
            <View style={styles.summaryGrid}>
              <View style={styles.summaryItem}>
                <Text style={styles.summaryLabel}>Mood</Text>
                <Text style={styles.summaryValue}>{mood ? mood.charAt(0).toUpperCase() + mood.slice(1) : 'Any'}</Text>
              </View>
              <View style={styles.summaryItem}>
                <Text style={styles.summaryLabel}>Activity</Text>
                <Text style={styles.summaryValue}>{activity ? activity.charAt(0).toUpperCase() + activity.slice(1).replace('_', ' ') : 'Any'}</Text>
              </View>
              <View style={styles.summaryItem}>
                <Text style={styles.summaryLabel}>Lyrics</Text>
                <Text style={styles.summaryValue}>{getLyricLabel(lyricPreference)}</Text>
              </View>
              <View style={styles.summaryItem}>
                <Text style={styles.summaryLabel}>Songs</Text>
                <Text style={styles.summaryValue}>{playlist.length} tracks</Text>
              </View>
            </View>
          </LinearGradient>

          {/* Info Banner */}
          <View style={styles.infoBanner}>
            <Text style={styles.infoText}>
              No exact activity match found. Showing best mood-based recommendations.
            </Text>
          </View>

          {/* Song List */}
          <View style={styles.songList}>
            {playlist.length === 0 ? (
               <Text style={{textAlign: 'center', marginTop: 20, color: '#6b7280'}}>No songs found for this configuration.</Text>
            ) : (
              playlist.map((song) => (
                <View key={song.id} style={styles.songCard}>
                  
                  <View style={styles.songInfoRow}>
                    <View style={styles.songImagePlaceholder}>
                      <Feather name="music" size={32} color="#9ca3af" />
                    </View>
                    <View style={styles.songDetails}>
                      <Text style={styles.songTitle}>{song.title}</Text>
                      <Text style={styles.songArtist}>{song.artist}</Text>
                      
                      <View style={styles.tagRow}>
                        <View style={styles.tag}>
                           <Text style={styles.tagText}>{song.bpm} BPM</Text>
                        </View>
                        <View style={styles.tagAccent}>
                           <Text style={styles.tagTextAccent}>{song.mood}</Text>
                        </View>
                      </View>
                    </View>
                  </View>

                  <View style={styles.actionRow}>
                    <TouchableOpacity style={styles.spotifyButton}>
                      <Feather name="play" size={16} color="#ffffff" style={{ marginRight: 8 }} />
                      <Text style={styles.spotifyButtonText}>Play on Spotify</Text>
                    </TouchableOpacity>
                    
                    <TouchableOpacity style={styles.helpButton}>
                      <Feather name="help-circle" size={20} color="#4b5563" />
                    </TouchableOpacity>
                  </View>

                </View>
              ))
            )}
          </View>

          {/* Bottom spacing for fixed button */}
          <View style={{ height: 120 }} />
        </ScrollView>

        {/* Bottom Fixed Area */}
        <LinearGradient
          colors={['rgba(255,255,255,0)', 'rgba(255,255,255,0.9)', '#ffffff']}
          style={styles.bottomGradient}
          pointerEvents="box-none"
        >
          <TouchableOpacity style={styles.rateButtonContainer} activeOpacity={0.9}>
            <LinearGradient
              colors={['#CC00FF', '#E4007C']}
              start={{ x: 0, y: 0 }}
              end={{ x: 1, y: 0 }}
              style={styles.rateButton}
            >
              <Feather name="star" size={20} color="#ffffff" style={{ marginRight: 8 }} />
              <Text style={styles.rateButtonText}>Rate This Playlist</Text>
            </LinearGradient>
          </TouchableOpacity>
        </LinearGradient>

      </SafeAreaView>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  safeArea: {
    flex: 1,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingTop: 10,
    paddingBottom: 20,
  },
  iconButton: {
    width: 44,
    height: 44,
    justifyContent: 'center',
    alignItems: 'center',
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: '800',
    color: '#1f2937',
  },
  scrollContent: {
    paddingHorizontal: 20,
    paddingBottom: 40,
  },
  summaryCard: {
    borderRadius: 24,
    padding: 24,
    marginBottom: 20,
    shadowColor: '#F97316',
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.3,
    shadowRadius: 16,
    elevation: 8,
  },
  summaryTitle: {
    fontSize: 24,
    fontWeight: '800',
    color: '#ffffff',
    marginBottom: 24,
  },
  summaryGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    rowGap: 20,
  },
  summaryItem: {
    width: '50%',
  },
  summaryLabel: {
    fontSize: 14,
    color: 'rgba(255, 255, 255, 0.8)',
    marginBottom: 4,
  },
  summaryValue: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#ffffff',
  },
  infoBanner: {
    backgroundColor: '#E0F2FE',
    borderWidth: 1,
    borderColor: '#BAE6FD',
    borderRadius: 16,
    padding: 16,
    marginBottom: 24,
  },
  infoText: {
    fontSize: 14,
    color: '#0284C7',
    lineHeight: 20,
    fontWeight: '500',
  },
  songList: {
    gap: 16, // Assuming React Native >= 0.71, alternatively use marginBottom on child
  },
  songCard: {
    backgroundColor: '#ffffff',
    borderRadius: 20,
    padding: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.05,
    shadowRadius: 10,
    elevation: 3,
    borderWidth: 1,
    borderColor: '#f9fafb',
    marginBottom: 16, // Fallback for gap
  },
  songInfoRow: {
    flexDirection: 'row',
    marginBottom: 16,
  },
  songImagePlaceholder: {
    width: 80,
    height: 80,
    borderRadius: 12,
    marginRight: 16,
    backgroundColor: '#f3f4f6',
    justifyContent: 'center',
    alignItems: 'center',
  },
  songDetails: {
    flex: 1,
    justifyContent: 'center',
  },
  songTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: '#1f2937',
    marginBottom: 4,
  },
  songArtist: {
    fontSize: 14,
    color: '#6b7280',
    marginBottom: 8,
  },
  tagRow: {
    flexDirection: 'row',
    gap: 8,
  },
  tag: {
    backgroundColor: '#F3E8FF',
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 12,
    marginRight: 8, // fallback for gap
  },
  tagText: {
    fontSize: 12,
    color: '#A855F7',
    fontWeight: '600',
  },
  tagAccent: {
    backgroundColor: '#fce7f3',
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 12,
    marginRight: 8,
  },
  tagTextAccent: {
    fontSize: 12,
    color: '#be185d',
    fontWeight: '600',
  },
  actionRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    gap: 12,
  },
  spotifyButton: {
    flex: 1,
    flexDirection: 'row',
    backgroundColor: '#1DB954',
    paddingVertical: 14,
    borderRadius: 12,
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#1DB954',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.2,
    shadowRadius: 8,
    elevation: 2,
  },
  spotifyButtonText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: '700',
  },
  helpButton: {
    width: 48,
    height: 48,
    borderRadius: 12,
    backgroundColor: '#f3f4f6',
    justifyContent: 'center',
    alignItems: 'center',
  },
  bottomGradient: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    height: 140,
    justifyContent: 'flex-end',
    paddingHorizontal: 24,
    paddingBottom: 34,
  },
  rateButtonContainer: {
    shadowColor: '#CC00FF',
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.3,
    shadowRadius: 16,
    elevation: 8,
  },
  rateButton: {
    flexDirection: 'row',
    height: 60,
    borderRadius: 30,
    justifyContent: 'center',
    alignItems: 'center',
  },
  rateButtonText: {
    color: '#ffffff',
    fontSize: 18,
    fontWeight: 'bold',
  },
});

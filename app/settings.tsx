import { View, Text, StyleSheet, TouchableOpacity, ScrollView } from 'react-native';
import React from 'react';
import { router } from 'expo-router';
import { LinearGradient } from 'expo-linear-gradient';
import { Feather } from '@expo/vector-icons';
import { SafeAreaView } from 'react-native-safe-area-context';

export default function SettingsScreen() {
  const handleNavigation = (route: string) => {
    // Only 'about' is fully mocked for this demo.
    if (route === '/about') {
      router.push(route);
    } else {
      console.log(`Navigate to ${route} (Not implemented in demo)`);
    }
  };

  return (
    <LinearGradient 
      colors={['#faf5ff', '#fdfaff', '#ffffff']} 
      style={styles.container}
    >
      <SafeAreaView style={styles.safeArea}>
        
        {/* Header */}
        <View style={styles.header}>
          <TouchableOpacity 
            style={styles.backButton}
            onPress={() => router.back()}
          >
            <Feather name="chevron-left" size={24} color="#374151" />
          </TouchableOpacity>
          <Text style={styles.headerTitle}>Settings</Text>
          {/* Invisible view to balance flex space */}
          <View style={{ width: 44 }} />
        </View>

        {/* Scroll Content */}
        <ScrollView 
          showsVerticalScrollIndicator={false}
          contentContainerStyle={styles.scrollContent}
        >
          {/* Setting Items Container */}
          <View style={styles.menuContainer}>
            
            {/* Appearance */}
            <TouchableOpacity 
              style={styles.menuItem} 
              activeOpacity={0.7}
              onPress={() => handleNavigation('/appearance')}
            >
              <LinearGradient
                colors={['#CC00FF', '#E4007C']}
                start={{ x: 0, y: 0 }}
                end={{ x: 1, y: 1 }}
                style={styles.iconContainer}
              >
                <Feather name="sun" size={20} color="#ffffff" />
              </LinearGradient>
              <View style={styles.menuTextContainer}>
                <Text style={styles.menuTitle}>Appearance</Text>
                <Text style={styles.menuSubtitle}>Light</Text>
              </View>
              <Feather name="chevron-right" size={20} color="#9ca3af" />
            </TouchableOpacity>

            {/* Default Lyric Preference */}
            <TouchableOpacity 
              style={styles.menuItem} 
              activeOpacity={0.7}
              onPress={() => handleNavigation('/lyric-preference')}
            >
              <LinearGradient
                colors={['#CC00FF', '#E4007C']}
                start={{ x: 0, y: 0 }}
                end={{ x: 1, y: 1 }}
                style={styles.iconContainer}
              >
                <Feather name="music" size={20} color="#ffffff" />
              </LinearGradient>
              <View style={styles.menuTextContainer}>
                <Text style={styles.menuTitle}>Default Lyric Preference</Text>
                <Text style={styles.menuSubtitle}>No Preference</Text>
              </View>
              <Feather name="chevron-right" size={20} color="#9ca3af" />
            </TouchableOpacity>

            {/* Default Playlist Length */}
            <TouchableOpacity 
              style={styles.menuItem} 
              activeOpacity={0.7}
              onPress={() => handleNavigation('/playlist-length')}
            >
              <LinearGradient
                colors={['#CC00FF', '#E4007C']}
                start={{ x: 0, y: 0 }}
                end={{ x: 1, y: 1 }}
                style={styles.iconContainer}
              >
                <Feather name="list" size={20} color="#ffffff" />
              </LinearGradient>
              <View style={styles.menuTextContainer}>
                <Text style={styles.menuTitle}>Default Playlist Length</Text>
                <Text style={styles.menuSubtitle}>10 songs</Text>
              </View>
              <Feather name="chevron-right" size={20} color="#9ca3af" />
            </TouchableOpacity>

            {/* Reset Preferences */}
            <TouchableOpacity 
              style={styles.menuItemReset} 
              activeOpacity={0.7}
              onPress={() => console.log('Reset Preferences triggered')}
            >
              <View style={styles.iconContainerReset}>
                <Feather name="refresh-ccw" size={20} color="#EF4444" />
              </View>
              <View style={styles.menuTextContainer}>
                <Text style={styles.menuTitleReset}>Reset Preferences</Text>
              </View>
              <Feather name="chevron-right" size={20} color="#9ca3af" />
            </TouchableOpacity>

             {/* About MoodBeats */}
             <TouchableOpacity 
              style={styles.menuItem} 
              activeOpacity={0.7}
              onPress={() => handleNavigation('/about')}
            >
              <LinearGradient
                colors={['#CC00FF', '#E4007C']}
                start={{ x: 0, y: 0 }}
                end={{ x: 1, y: 1 }}
                style={styles.iconContainer}
              >
                <Feather name="info" size={20} color="#ffffff" />
              </LinearGradient>
              <View style={styles.menuTextContainer}>
                <Text style={styles.menuTitle}>About MoodBeats</Text>
              </View>
              <Feather name="chevron-right" size={20} color="#9ca3af" />
            </TouchableOpacity>

          </View>
          
          {/* Version Footer */}
          <View style={styles.footer}>
            <Text style={styles.footerVersion}>MoodBeats v1.0.0</Text>
            <Text style={styles.footerSubtitle}>Music that understands your mood</Text>
          </View>

        </ScrollView>
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
    paddingBottom: 24,
  },
  backButton: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: '#ffffff',
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 8,
    elevation: 2,
    borderWidth: 1,
    borderColor: '#f9fafb',
  },
  headerTitle: {
    fontSize: 22,
    fontWeight: '800',
    color: '#1f2937',
  },
  scrollContent: {
    paddingHorizontal: 20,
    paddingBottom: 40,
  },
  menuContainer: {
    gap: 16, // If RN < 0.71, use marginBottom on children instead
  },
  menuItem: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#ffffff',
    padding: 16,
    borderRadius: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.03,
    shadowRadius: 10,
    elevation: 2,
    borderWidth: 1,
    borderColor: '#f9fafb',
    marginBottom: 16, // fallback
  },
  menuItemReset: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#ffffff',
    padding: 16,
    borderRadius: 20,
    shadowColor: '#EF4444',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.06,
    shadowRadius: 10,
    elevation: 2,
    borderWidth: 1,
    borderColor: '#FEF2F2',
    marginBottom: 16, // fallback
  },
  iconContainer: {
    width: 48,
    height: 48,
    borderRadius: 24,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 16,
  },
  iconContainerReset: {
    width: 48,
    height: 48,
    borderRadius: 24,
    backgroundColor: '#FEF2F2',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 16,
  },
  menuTextContainer: {
    flex: 1,
    justifyContent: 'center',
  },
  menuTitle: {
    fontSize: 16,
    fontWeight: '700',
    color: '#1f2937',
  },
  menuTitleReset: {
    fontSize: 16,
    fontWeight: '700',
    color: '#EF4444',
  },
  menuSubtitle: {
    fontSize: 14,
    color: '#6b7280',
    marginTop: 2,
    fontWeight: '500',
  },
  footer: {
    marginTop: 40,
    alignItems: 'center',
  },
  footerVersion: {
    fontSize: 14,
    fontWeight: '600',
    color: '#9ca3af',
    marginBottom: 4,
  },
  footerSubtitle: {
    fontSize: 12,
    color: '#d1d5db',
  }
});

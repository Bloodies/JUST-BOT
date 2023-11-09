import asyncio
import ephem


async def get_moon_position(longitude, latitude, date_str, time_str):
    observer = ephem.Observer()
    observer.lon = str(longitude)  # Долгота наблюдателя
    observer.lat = str(latitude)  # Широта наблюдателя
    observer.date = f'{date_str} {time_str}'  # Дата и время

    moon = ephem.Moon(observer)
    moon.compute(observer)

    return {
        'altitude': moon.alt,
        'azimuth': moon.az,
        'phase': moon.phase,
        'distance': moon.earth_distance,
        'ra': moon.ra,
        'dec': moon.dec
    }


async def run():
    res = await get_moon_position(57.997917787933865, 56.266396273013, '1999-01-01', '20:00')
    print(res)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(run())
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
